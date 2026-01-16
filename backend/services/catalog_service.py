from sqlmodel import Session
from sqlalchemy import text
from backend.database import engine
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from backend.services.scrapers.category_kabum import scrape_kabum_category
from backend.services.scrapers.category_pichau import scrape_pichau_category
from backend.services.scrapers.category_terabyte import scrape_terabyte_category
from backend.services.scrapers.categories import CATEGORIES
from backend.services.scrapers import amazon, kabum, pichau, terabyte

def catalog_products_by_category(category: str, store: str = None):
    """
    Catalogs products from a specific category
    If store is None, catalogs from all stores
    """
    scrapers = {
        'kabum': scrape_kabum_category,
        'pichau': scrape_pichau_category,
        'terabyte': scrape_terabyte_category
    }
    
    stores_to_scrape = [store] if store else scrapers.keys()
    total_added = 0
    
    for store_name in stores_to_scrape:
        if store_name not in scrapers:
            continue
        
        print(f"Cataloging {category} from {store_name}...")
        
        try:
            scraper = scrapers[store_name]
            products = scraper(category, max_products=500)
            
            for product_data in products:
                try:
                    _save_catalog_product(product_data)
                    total_added += 1
                except Exception as e:
                    print(f"Error saving product {product_data.get('name')}: {e}")
            
            print(f"✓ Cataloged {len(products)} products from {store_name}")
        
        except Exception as e:
            print(f"✗ Error cataloging {category} from {store_name}: {e}")
    
    return total_added

def catalog_all_products():
    """
    Catalogs all categories from all stores
    """
    print("=== Starting Full Catalog Update ===")
    total = 0
    
    for category in CATEGORIES:
        print(f"\n--- Cataloging {category} ---")
        count = catalog_products_by_category(category)
        total += count
        print(f"Added {count} products for {category}")
    
    print(f"\n=== Catalog Update Complete: {total} products added ===")
    return total

def _save_catalog_product(product_data: dict):
    """
    Saves or updates a product in the catalog (without price)
    """
    with Session(engine) as session:
        # Check if product exists
        check_query = text("SELECT id FROM product WHERE url = :url")
        result = session.execute(check_query, {"url": product_data['url']})
        existing = result.fetchone()
        
        if existing:
            # Update existing product
            update_query = text("""
                UPDATE product 
                SET name = :name, 
                    category = :category,
                    last_updated = :last_updated
                WHERE url = :url
            """)
            session.execute(update_query, {
                "name": product_data['name'],
                "category": product_data['category'],
                "last_updated": datetime.utcnow(),
                "url": product_data['url']
            })
        else:
            # Insert new product (without price)
            insert_query = text("""
                INSERT INTO product (url, name, store, category, current_price, last_updated)
                VALUES (:url, :name, :store, :category, :current_price, :last_updated)
            """)
            session.execute(insert_query, {
                "url": product_data['url'],
                "name": product_data['name'],
                "store": product_data['store'],
                "category": product_data['category'],
                "current_price": 0.0,  # Price will be 0 until fetched
                "last_updated": datetime.utcnow()
            })
        
        session.commit()

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from backend.services.scrapers import amazon, kabum, pichau, terabyte

# ... imports ...

def update_product_price(product):
    """
    Updates the price of a single product by scraping its URL.
    Returns the updated product dict or the original if failed.
    """
    store = product['store']
    url = product['url']
    
    scraper_map = {
        'amazon': amazon,
        'kabum': kabum,
        'pichau': pichau,
        'terabyte': terabyte
    }
    
    if store not in scraper_map:
        return product
        
    try:
        # Scrape
        result = scraper_map[store].fetch_product(url)
        if result and result.get('price') is not None:
            # Update DB (Quick session)
            with Session(engine) as session:
                update_query = text("""
                    UPDATE product 
                    SET current_price = :price, last_updated = :updated
                    WHERE id = :id
                """)
                session.execute(update_query, {
                    "price": result['price'],
                    "updated": datetime.utcnow(),
                    "id": product['id']
                })
                # Add History
                hist_query = text("""
                    INSERT INTO pricehistory (product_id, price, timestamp)
                    VALUES (:pid, :price, :ts)
                """)
                session.execute(hist_query, {
                    "pid": product['id'],
                    "price": result['price'],
                    "ts": datetime.utcnow()
                })
                session.commit()
            
            # Update local dict
            product['current_price'] = result['price']
            product['last_updated'] = datetime.utcnow()
            
    except Exception as e:
        print(f"Error updating price for {product['name']}: {e}")
        
    return product

def search_catalog(query: str, category: str = None, store: str = None, limit: int = 20):
    """
    Searches the product catalog and updates prices if stale (>1h)
    """
    # 1. Return empty if no filters (Initial State)
    if not query and not category and not store:
        return []

    with Session(engine) as session:
        sql = "SELECT id, name, url, store, category, current_price, last_updated, image_url FROM product WHERE 1=1"
        params = {}
        
        if query:
            sql += " AND LOWER(name) LIKE LOWER(:query)"
            params['query'] = f"%{query}%"
        
        if category:
            sql += " AND category = :category"
            params['category'] = category
        
        if store:
            sql += " AND store = :store"
            params['store'] = store
        
        sql += f" ORDER BY name LIMIT {limit}"
        
        result = session.execute(text(sql), params)
        rows = result.fetchall()
        
        products = []
        products_to_update = []
        
        for row in rows:
            p_dict = {
                "id": row[0],
                "name": row[1],
                "url": row[2],
                "store": row[3],
                "category": row[4],
                "current_price": row[5],
                "last_updated": row[6],
                "image_url": row[7]
            }
            products.append(p_dict)
            
            # Check freshness (1 hour)
            last_up = row[6]
            if not last_up:
                last_up = datetime.min
            elif isinstance(last_up, str):
                try:
                    # Attempt to parse ISO format string from SQLite
                    last_up = datetime.fromisoformat(last_up)
                except ValueError:
                    # Fallback if format is different (e.g. without T separator)
                    try:
                        last_up = datetime.strptime(last_up, "%Y-%m-%d %H:%M:%S.%f")
                    except ValueError:
                        try:
                            last_up = datetime.strptime(last_up, "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            last_up = datetime.min

            is_stale = (datetime.utcnow() - last_up) > timedelta(hours=1)
            is_zero = row[5] == 0 or row[5] is None
            
            if is_stale or is_zero:
                products_to_update.append(p_dict)
        
        # 3. Parallel Update for stale products
        # Limit to avoid massive lag
        if products_to_update:
            print(f"Updating {len(products_to_update)} stale products...")
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(update_product_price, p): p for p in products_to_update}
                
                for future in as_completed(futures):
                    # Results are updated in-place in the dicts inside 'products' list
                    pass
                    
        return products

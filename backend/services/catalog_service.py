from sqlmodel import Session
from sqlalchemy import text
from database import engine
from datetime import datetime
from services.scrapers.category_kabum import scrape_kabum_category
from services.scrapers.category_pichau import scrape_pichau_category
from services.scrapers.category_terabyte import scrape_terabyte_category
from services.scrapers.categories import CATEGORIES

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

def search_catalog(query: str, category: str = None, store: str = None, limit: int = 20):
    """
    Searches the product catalog
    """
    with Session(engine) as session:
        sql = "SELECT id, name, url, store, category FROM product WHERE 1=1"
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
        for row in rows:
            products.append({
                "id": row[0],
                "name": row[1],
                "url": row[2],
                "store": row[3],
                "category": row[4]
            })
        
        return products

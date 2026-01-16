from sqlmodel import Session
from sqlalchemy import text
from database import engine
from models import Product, PriceHistory
from datetime import datetime

def save_product_history(data: dict) -> Product:
    """
    Saves or updates a product and records its price history.
    """
    if "error" in data:
        return None

    url = data["url"]
    price = data["price"]
    name = data["name"]
    store = data["store"]

    with Session(engine, expire_on_commit=False) as session:
        # 1. Check if product exists - SQL PURO
        query = text("SELECT * FROM product WHERE url = :url")
        result = session.execute(query, {"url": url})
        row = result.fetchone()
        
        if not row:
            # Create new product - SQL PURO
            insert_query = text("""
                INSERT INTO product (url, name, store, current_price, last_updated)
                VALUES (:url, :name, :store, :current_price, :last_updated)
            """)
            session.execute(insert_query, {
                "url": url,
                "name": name,
                "store": store,
                "current_price": price,
                "last_updated": datetime.utcnow()
            })
            session.commit()
            
            # Get the created product
            result = session.execute(query, {"url": url})
            row = result.fetchone()
            product_id = row[0]  # id é a primeira coluna
            current_price = row[4]  # current_price é a quinta coluna
        else:
            # Product exists
            product_id = row[0]
            current_price = row[4]
            
            # Update existing product if price changed - SQL PURO
            if current_price != price:
                update_query = text("""
                    UPDATE product 
                    SET current_price = :current_price, last_updated = :last_updated
                    WHERE id = :id
                """)
                session.execute(update_query, {
                    "current_price": price,
                    "last_updated": datetime.utcnow(),
                    "id": product_id
                })
                session.commit()

        # 2. Add Price History - SQL PURO
        # Check last history
        history_query = text("""
            SELECT * FROM pricehistory 
            WHERE product_id = :product_id 
            ORDER BY timestamp DESC 
            LIMIT 1
        """)
        history_result = session.execute(history_query, {"product_id": product_id})
        last_history_row = history_result.fetchone()

        should_save_history = False
        if not last_history_row:
            should_save_history = True
        elif last_history_row[2] != price:  # price é a terceira coluna (índice 2)
            should_save_history = True

        if should_save_history:
            insert_history_query = text("""
                INSERT INTO pricehistory (product_id, price, timestamp)
                VALUES (:product_id, :price, :timestamp)
            """)
            session.execute(insert_history_query, {
                "product_id": product_id,
                "price": price,
                "timestamp": datetime.utcnow()
            })
            session.commit()

        # Return product object (opcional, pode retornar None se não precisar)
        return None

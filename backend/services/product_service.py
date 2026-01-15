from sqlmodel import Session, select
from ..database import engine
from ..models import Product, PriceHistory
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
        # 1. Check if product exists
        statement = select(Product).where(Product.url == url)
        product = session.exec(statement).first()

        if not product:
            # Create new product
            product = Product(
                url=url,
                name=name,
                store=store,
                current_price=price,
                last_updated=datetime.utcnow()
            )
            session.add(product)
            session.commit()
            session.refresh(product)
        else:
            # Update existing product
            if product.current_price != price:
                product.current_price = price
                product.last_updated = datetime.utcnow()
                session.add(product)
                session.commit()
                session.refresh(product)

        # 2. Add Price History (Always, or optimized?)
        # For now, we save every check. Ideal: Save only if changed or > 24h.
        # Let's save only if price changed OR it's the first record
        
        # Check last history
        history_stmt = select(PriceHistory).where(PriceHistory.product_id == product.id).order_by(PriceHistory.timestamp.desc())
        last_history = session.exec(history_stmt).first()

        should_save_history = False
        if not last_history:
            should_save_history = True
        elif last_history.price != price:
            should_save_history = True
        
        # Force save if it's been a while? (Optional, let's keep it simple for now)

        if should_save_history:
            history = PriceHistory(
                product_id=product.id,
                price=price,
                timestamp=datetime.utcnow()
            )
            session.add(history)
            session.commit()

        return product

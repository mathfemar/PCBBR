from backend.services.product_service import save_product_history
from backend.database import get_session
from backend.models import Product, PriceHistory
from sqlmodel import select, Session
from backend.database import engine

def test_persistence():
    print("--- Testing Persistence ---")
    
    # Mock Scraped Data
    mock_data = {
        "name": "Test Product Persistence",
        "price": 999.99,
        "url": "https://example.com/test-product",
        "store": "TestStore"
    }

    # 1. Save
    print("Saving product...")
    product = save_product_history(mock_data)
    print(f"Product Saved: ID={product.id}, Name={product.name}")

    # 2. Verify in DB
    print("Verifying in DB...")
    with Session(engine) as session:
        # Check Product
        p = session.exec(select(Product).where(Product.url == mock_data["url"])).first()
        assert p is not None
        print(f"✅ Product found in DB: {p.name}")

        # Check History
        h = session.exec(select(PriceHistory).where(PriceHistory.product_id == p.id)).first()
        assert h is not None
        assert h.price == 999.99
        print(f"✅ PriceHistory found: {h.price} at {h.timestamp}")

        # 3. Update Price
        print("Updating price to 888.88...")
        mock_data["price"] = 888.88
        save_product_history(mock_data)
        
        # Check History Count
        histories = session.exec(select(PriceHistory).where(PriceHistory.product_id == p.id)).all()
        print(f"✅ History Count: {len(histories)} (Should be 2)")
        for hist in histories:
            print(f"   - {hist.price}")

if __name__ == "__main__":
    test_persistence()

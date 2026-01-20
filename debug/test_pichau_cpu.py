"""Quick test for Pichau CPU scraping"""
import sys
from pathlib import Path

backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from services.scrapers.category_pichau import scrape_pichau_category

print("Testing Pichau CPU scraping...")
products = scrape_pichau_category("CPU", max_products=10)
print(f"\nFound {len(products)} products:")
for p in products[:5]:
    print(f"  - {p['name']}")
    print(f"    URL: {p['url']}")
    print()

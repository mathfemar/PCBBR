from curl_cffi import requests
from bs4 import BeautifulSoup
import json
import re
from backend.services import utils as scrapers_utils

def fetch_product(url):
    """
    Fetches product details from TerabyteShop.
    Returns a dict with 'name', 'price', and 'url'.
    """
    try:
        # Use Chrome impersonation to bypass Cloudflare
        # verified working with "chrome120"
        response = requests.get(
            url, 
            impersonate="chrome120", 
            headers=scrapers_utils.get_headers(),
            timeout=15,
            verify=False
        )
        
        if response.status_code not in [200, 201]:
            return {"error": f"Status code {response.status_code}", "url": url}
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Strategy: Look for JSON-LD Structured Data
        # This is more reliable than CSS selectors
        scripts = soup.find_all('script', type='application/ld+json')
        
        product_data = None
        
        for script in scripts:
            try:
                data = json.loads(script.string)
                # JSON-LD can be a list or a dict
                if isinstance(data, list):
                    for item in data:
                        if item.get('@type') == 'Product':
                            product_data = item
                            break
                elif isinstance(data, dict):
                    if data.get('@type') == 'Product':
                        product_data = data
                
                if product_data:
                    break
            except (json.JSONDecodeError, TypeError):
                continue
                
        if product_data:
            name = product_data.get('name')
            offers = product_data.get('offers', {})
            price = offers.get('price')
            
            # Fallback if price is in a list of offers
            if not price and isinstance(offers, list):
                price = offers[0].get('price')
            
            # Extract Availability
            available = True
            avail_schema = offers.get('availability')
            if isinstance(offers, list) and not avail_schema:
                 avail_schema = offers[0].get('availability')

            if avail_schema:
                if 'OutOfStock' in avail_schema:
                    available = False

            return {
                "name": name,
                "price": scrapers_utils.clean_price(price),
                "url": url,
                "store": "TerabyteShop",
                "available": available
            }
        
        # Fallback Strategy: CSS Selectors (if JSON-LD fails)
        name_elem = soup.find('h1', class_='tit-prod')
        price_elem = soup.find('p', id='valVista')
        
        if name_elem and price_elem:
            return {
                "name": name_elem.get_text(strip=True),
                "price": scrapers_utils.clean_price(price_elem.get_text()),
                "url": url,
                "store": "TerabyteShop"
            }
            
        return {"error": "Could not extract data", "url": url}

    except Exception as e:
        return {"error": str(e), "url": url}

if __name__ == "__main__":
    # Test with the URL we investigated
    test_url = "https://www.terabyteshop.com.br/produto/16145/placa-mae-gigabyte-b550m-aorus-elite-chipset-b550-amd-am4-atx-ddr4"
    print(fetch_product(test_url))

from curl_cffi import requests
from bs4 import BeautifulSoup
import json
import scrapers_utils

def fetch_product(url):
    """
    Fetches product details from Kabum.
    Returns a dict with 'name', 'price', and 'url'.
    """
    try:
        # Use Chrome impersonation
        response = requests.get(
            url, 
            impersonate="chrome120", 
            headers=scrapers_utils.get_headers(),
            timeout=15
        )
        
        if response.status_code not in [200, 201]:
            return {"error": f"Status code {response.status_code}", "url": url}
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Strategy: Extract internal Next.js data
        next_data_tag = soup.find('script', id='__NEXT_DATA__')
        
        if next_data_tag:
            try:
                data = json.loads(next_data_tag.string)
                page_props = data.get('props', {}).get('pageProps', {})
                product = page_props.get('product', {})
                
                if product:
                    # Extract Name
                    name = product.get('title') or product.get('name')
                    
                    # Extract Price
                    # Kabum usually has a 'prices' object
                    prices = product.get('prices', {})
                    price = prices.get('priceWithDiscount') # Cash price (lower)
                    
                    if not price:
                        price = prices.get('price') # Normal price
                    
                    if not price:
                        # Fallback to direct price key
                        price = product.get('price')

                    if name and price:
                        return {
                            "name": name,
                            "price": scrapers_utils.clean_price(price),
                            "url": url,
                            "store": "Kabum"
                        }
            except Exception as e:
                pass # JSON parsing failed
        
        # Fallback Strategy: Meta Tags (Kabum sometimes uses them)
        price_meta = soup.find("meta", property="product:price:amount")
        name_meta = soup.find("meta", property="og:title")
        
        if price_meta and name_meta:
             return {
                "name": name_meta.get("content").replace(" | KaBuM!", "").strip(),
                "price": scrapers_utils.clean_price(price_meta.get("content")),
                "url": url,
                "store": "Kabum"
            }

        return {"error": "Could not extract data (Kabum structure changed)", "url": url}

    except Exception as e:
        return {"error": str(e), "url": url}

if __name__ == "__main__":
    test_url = "https://www.kabum.com.br/produto/609956/processador-amd-ryzen-5-9600x-3-9-ghz-5-4-ghz-cache-32-mb-6-nucleos-12-threads-am5-100-100001405wof"
    print(fetch_product(test_url))

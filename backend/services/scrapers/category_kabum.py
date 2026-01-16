from curl_cffi import requests
from bs4 import BeautifulSoup
from services.scrapers.categories import CATEGORY_URLS
import time
import json

def scrape_kabum_category(category: str, max_products: int = 500):
    """
    Scrapes product listings from Kabum category pages with pagination
    Kabum uses Next.js with JSON data embedded in script tags
    Returns list of {name, url, store, category}
    """
    if category not in CATEGORY_URLS['kabum']:
        return []
    
    base_url = CATEGORY_URLS['kabum'][category]
    products = []
    seen_urls = set()
    page = 1
    
    try:
        while len(products) < max_products:
            # Kabum usa ?pagina=N para paginação
            if page == 1:
                url = base_url
            else:
                url = f"{base_url}?pagina={page}"
            
            print(f"Scraping Kabum {category} page {page}...")
            
            response = requests.get(
                url,
                impersonate="chrome120",
                timeout=15,
                verify=False
            )
            
            if response.status_code != 200:
                break
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Kabum usa Next.js com dados em JSON
            scripts = soup.find_all('script')
            catalog_data = None
            
            for script in scripts:
                if script.string and 'catalogServer' in script.string:
                    try:
                        data = json.loads(script.string)
                        inner_json_str = data['props']['pageProps']['data']
                        inner_data = json.loads(inner_json_str)
                        catalog_data = inner_data['catalogServer']['data']
                        break
                    except:
                        continue
            
            if not catalog_data:
                break
            
            page_products = 0
            for item in catalog_data:
                if len(products) >= max_products:
                    break
                    
                try:
                    code = item.get('code')
                    name = item.get('name')
                    friendly_name = item.get('friendlyName', '')
                    
                    if not code or not name:
                        continue
                    
                    # Construir URL do produto
                    product_url = f"https://www.kabum.com.br/produto/{code}/{friendly_name}"
                    
                    # Evitar duplicatas
                    if product_url in seen_urls:
                        continue
                    seen_urls.add(product_url)
                    
                    products.append({
                        'name': name,
                        'url': product_url,
                        'store': 'kabum',
                        'category': category
                    })
                    page_products += 1
                except Exception as e:
                    print(f"Error parsing Kabum product: {e}")
                    continue
            
            if page_products == 0:
                break
            
            page += 1
            time.sleep(1)  # Rate limiting
        
        return products
    
    except Exception as e:
        print(f"Error scraping Kabum category {category}: {e}")
        return products

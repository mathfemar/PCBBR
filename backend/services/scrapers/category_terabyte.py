from curl_cffi import requests
from bs4 import BeautifulSoup
from services.scrapers.categories import CATEGORY_URLS
import time

def scrape_terabyte_category(category: str, max_products: int = 500):
    """
    Scrapes product listings from Terabyte category pages with pagination
    Returns list of {name, url, store, category}
    """
    if category not in CATEGORY_URLS['terabyte']:
        return []
    
    base_url = CATEGORY_URLS['terabyte'][category]
    products = []
    seen_urls = set()
    page = 1
    
    try:
        while len(products) < max_products:
            # Terabyte usa ?page=N para paginação
            if page == 1:
                url = base_url
            else:
                url = f"{base_url}?page={page}"
            
            print(f"Scraping Terabyte {category} page {page}...")
            
            response = requests.get(
                url,
                impersonate="chrome120",
                timeout=15,
                verify=False
            )
            
            if response.status_code != 200 and response.status_code != 201:
                break
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Terabyte usa divs com classe product-item
            product_items = soup.find_all('div', class_='product-item')
            
            if not product_items:
                break
            
            page_products = 0
            for item in product_items:
                if len(products) >= max_products:
                    break
                    
                try:
                    # Link e nome do produto
                    link_tag = item.find('a', class_='product-item__name')
                    if not link_tag:
                        # Tentar alternativa
                        link_tag = item.find('a', href=True)
                    
                    if not link_tag:
                        continue
                    
                    product_url = link_tag.get('href')
                    if not product_url.startswith('http'):
                        product_url = 'https://www.terabyteshop.com.br' + product_url
                    
                    # Evitar duplicatas
                    if product_url in seen_urls:
                        continue
                    seen_urls.add(product_url)
                    
                    # Nome do produto
                    name = link_tag.get_text(strip=True)
                    
                    if not name:
                        continue
                    
                    products.append({
                        'name': name,
                        'url': product_url,
                        'store': 'terabyte',
                        'category': category
                    })
                    page_products += 1
                except Exception as e:
                    print(f"Error parsing Terabyte product: {e}")
                    continue
            
            if page_products == 0:
                break
            
            page += 1
            time.sleep(1)  # Rate limiting
        
        return products
    
    except Exception as e:
        print(f"Error scraping Terabyte category {category}: {e}")
        return products

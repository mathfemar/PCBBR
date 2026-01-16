from curl_cffi import requests
from bs4 import BeautifulSoup
from services.scrapers.categories import CATEGORY_URLS
import time

def scrape_pichau_category(category: str, max_products: int = 500):
    """
    Scrapes product listings from Pichau category pages (with pagination)
    Returns list of {name, url, store, category}
    """
    if category not in CATEGORY_URLS['pichau']:
        return []
    
    base_url = CATEGORY_URLS['pichau'][category]
    products = []
    seen_urls = set()  # Para evitar duplicatas
    page = 1
    
    while len(products) < max_products:
        try:
            # Pichau usa ?page=N para paginação
            url = f"{base_url}?page={page}"
            print(f"Scraping Pichau {category} page {page}...")
            
            response = requests.get(
                url,
                impersonate="chrome120",
                timeout=15,
                verify=False
            )
            
            if response.status_code != 200:
                print(f"Failed to fetch page {page}, status: {response.status_code}")
                break
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Pichau usa links diretos que começam com /processador-, /placa-, etc
            product_links = soup.find_all('a', href=lambda x: x and (
                x.startswith('/processador-') or 
                x.startswith('/placa-') or 
                x.startswith('/memoria-') or
                x.startswith('/ssd-') or
                x.startswith('/cooler-') or
                x.startswith('/fonte-') or
                x.startswith('/gabinete-') or
                x.startswith('/monitor-')
            ))
            
            if not product_links:
                print(f"No products found on page {page}, stopping pagination")
                break
            
            page_products = 0
            for link_tag in product_links:
                try:
                    product_url = link_tag['href']
                    if not product_url.startswith('http'):
                        product_url = 'https://www.pichau.com.br' + product_url
                    
                    # Evitar duplicatas
                    if product_url in seen_urls:
                        continue
                    seen_urls.add(product_url)
                    
                    # Nome do produto está no alt da imagem dentro do link
                    img_tag = link_tag.find('img', alt=True)
                    if not img_tag:
                        continue
                    
                    name = img_tag['alt'].strip()
                    if not name:
                        continue
                    
                    products.append({
                        'name': name,
                        'url': product_url,
                        'store': 'pichau',
                        'category': category
                    })
                    page_products += 1
                    
                    if len(products) >= max_products:
                        break
                        
                except Exception as e:
                    print(f"Error parsing Pichau product: {e}")
                    continue
            
            print(f"Found {page_products} products on page {page} (total: {len(products)})")
            
            # Se não encontrou produtos novos nesta página, parar
            if page_products == 0:
                break
            
            # Delay entre páginas para não sobrecarregar
            time.sleep(1)
            page += 1
            
        except Exception as e:
            print(f"Error scraping Pichau page {page}: {e}")
            break
    
    print(f"Total products scraped: {len(products)}")
    return products

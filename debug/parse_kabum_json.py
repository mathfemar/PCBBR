import re
import json
from bs4 import BeautifulSoup

html = open('kabum_sample.html', 'r', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')

# Encontrar o script com os dados
scripts = soup.find_all('script')
for script in scripts:
    text = script.string
    if text and 'catalogServer' in text:
        # Extrair o JSON
        try:
            # O script contém: {"props":{"pageProps":{"data":"{\"catalogServer\":...}"}}}
            data = json.loads(text)
            
            # Pegar o data que está como string JSON dentro do JSON
            inner_json_str = data['props']['pageProps']['data']
            inner_data = json.loads(inner_json_str)
            
            # Extrair produtos
            if 'catalogServer' in inner_data and 'data' in inner_data['catalogServer']:
                products = inner_data['catalogServer']['data']
                print(f"Found {len(products)} products!")
                
                # Mostrar primeiro produto
                if products:
                    p = products[0]
                    print(f"\nFirst product structure:")
                    print(f"  Code: {p.get('code')}")
                    print(f"  Name: {p.get('name')}")
                    print(f"  URL: {p.get('url')}")
                    print(f"  Image: {p.get('img')}")
                    print(f"  Price: {p.get('priceWithDiscount')}")
                    print(f"\nAll keys: {list(p.keys())}")
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            import traceback
            traceback.print_exc()

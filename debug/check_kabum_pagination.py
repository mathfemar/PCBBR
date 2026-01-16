import json
from bs4 import BeautifulSoup

html = open('kabum_sample.html', 'r', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')

script = [s.string for s in soup.find_all('script') if s.string and 'catalogServer' in s.string][0]
data = json.loads(script)
inner = json.loads(data['props']['pageProps']['data'])
products = inner['catalogServer']['data']

print(f"Total products: {len(products)}\n")

for i, p in enumerate(products[:3]):
    print(f"Product {i+1}:")
    print(f"  Code: {p['code']}")
    print(f"  Name: {p['name'][:60]}...")
    print(f"  FriendlyName: {p.get('friendlyName', 'N/A')}")
    print(f"  URL: https://www.kabum.com.br/produto/{p['code']}/{p.get('friendlyName', '')}")
    print()

# Verificar paginação
meta = inner['catalogServer']['meta']
print(f"Total items: {meta.get('totalItemsCount')}")
print(f"Page size: {meta.get('page', {}).get('size')}")
print(f"Current page: {meta.get('page', {}).get('current')}")

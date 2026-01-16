import re
from bs4 import BeautifulSoup

html = open('kabum_sample.html', 'r', encoding='utf-8').read()

# Procurar por scripts que contenham dados
soup = BeautifulSoup(html, 'html.parser')
scripts = soup.find_all('script')

print(f"Total scripts: {len(scripts)}")

# Procurar por JSON com produtos
for i, script in enumerate(scripts):
    text = script.string
    if text and ('produto' in text.lower() or 'product' in text.lower()):
        print(f"\n=== Script {i} (first 500 chars) ===")
        print(text[:500])
        if 'href' in text or 'url' in text.lower():
            print("^^^ This one has URLs! ^^^")
            
# Procurar por divs/articles com produtos
articles = soup.find_all(['article', 'div'], attrs={'data-product': True})
print(f"\n\nElements with data-product: {len(articles)}")

# Procurar por links de produtos
all_links = soup.find_all('a', href=True)
product_links = [a for a in all_links if '/produto/' in a.get('href', '')]
print(f"Links to /produto/: {len(product_links)}")

if product_links:
    print("\nFirst 3 product links:")
    for link in product_links[:3]:
        print(f"  - {link.get('href')}")
        print(f"    Text: {link.get_text(strip=True)[:60]}")

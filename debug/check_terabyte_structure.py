from bs4 import BeautifulSoup

html = open('terabyte_sample.html', 'r', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')

# Procurar pela estrutura product-item
product_items = soup.find_all('div', class_='product-item')
print(f"Found {len(product_items)} product items")

if product_items:
    item = product_items[0]
    print("\nFirst product structure:")
    
    # Link
    link = item.find('a', href=True)
    if link:
        print(f"  URL: {link.get('href')}")
        
    # Nome
    name_elem = item.find('a', class_='product-item__name')
    if name_elem:
        print(f"  Name: {name_elem.get_text(strip=True)}")
    
    # Imagem
    img = item.find('img')
    if img:
        print(f"  Image: {img.get('src') or img.get('data-src')}")
    
    print("\n  All classes in this item:")
    for elem in item.find_all(class_=True):
        print(f"    {elem.name}: {elem.get('class')}")

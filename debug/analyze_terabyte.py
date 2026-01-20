from bs4 import BeautifulSoup

html = open('terabyte_sample.html', 'r', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')

# Procurar por links de produtos
all_links = soup.find_all('a', href=True)
product_links = [a for a in all_links if 'produto' in a.get('href', '').lower() or 'prod.php' in a.get('href', '').lower()]
print(f"Product links found: {len(product_links)}")

if product_links:
    print("\nFirst 3 product links:")
    for i, link in enumerate(product_links[:3]):
        print(f"\n{i+1}. URL: {link.get('href')}")
        print(f"   Text: {link.get_text(strip=True)[:80]}")
        print(f"   Parent: {link.parent.name}")
        print(f"   Parent classes: {link.parent.get('class', [])}")

# Procurar por divs com produtos
divs_with_product = soup.find_all('div', class_=lambda x: x and ('product' in str(x).lower() or 'pbox' in str(x).lower()))
print(f"\n\nDivs with product-like classes: {len(divs_with_product)}")
if divs_with_product:
    print("Sample classes:", [d.get('class') for d in divs_with_product[:3]])

# Procurar por qualquer estrutura repetida
all_divs = soup.find_all('div', class_=True)
class_counts = {}
for div in all_divs:
    classes = ' '.join(div.get('class', []))
    class_counts[classes] = class_counts.get(classes, 0) + 1

# Mostrar classes mais comuns (possivelmente produtos)
top_classes = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)[:10]
print("\n\nMost common div classes:")
for cls, count in top_classes:
    if count > 5 and count < 100:  # Provavelmente produtos
        print(f"  {count}x: {cls[:100]}")

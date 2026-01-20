from bs4 import BeautifulSoup

soup = BeautifulSoup(open('pichau_cpu_page.html', encoding='utf-8').read(), 'html.parser')

print("=== All Links ===")
links = soup.find_all('a', href=True)
for i, link in enumerate(links[:30]):
    href = link.get('href')
    text = link.get_text(strip=True)[:50]
    print(f"{i+1}. {href[:80]} | {text}")

print("\n=== Divs with 'product' class ===")
product_divs = soup.find_all('div', class_=lambda x: x and 'product' in x.lower())
if product_divs:
    first_product = product_divs[0]
    print(f"Class: {first_product.get('class')}")
    print(f"HTML (first 500 chars):\n{str(first_product)[:500]}")

"""Debug Pichau HTML to understand structure"""
from curl_cffi import requests
from bs4 import BeautifulSoup

url = 'https://www.pichau.com.br/hardware/processadores'

print("Fetching URL:", url)
response = requests.get(
    url,
    impersonate="chrome120",
    timeout=15,
    verify=False
)

print(f"Status: {response.status_code}")
print(f"Content length: {len(response.text)}")

with open('pichau_cpu_page.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

print("\nSaved to pichau_cpu_page.html")

soup = BeautifulSoup(response.text, 'html.parser')

# Procurar por diferentes padrões comuns
print("\n=== Looking for product patterns ===")
print(f"Divs with 'product': {len(soup.find_all('div', class_=lambda x: x and 'product' in x.lower()))}")
print(f"Divs with 'card': {len(soup.find_all('div', class_=lambda x: x and 'card' in x.lower()))}")
print(f"Divs with 'item': {len(soup.find_all('div', class_=lambda x: x and 'item' in x.lower()))}")
print(f"Links to /produto/: {len(soup.find_all('a', href=lambda x: x and '/produto/' in x))}")

# Sample primeiro produto se existir
product_links = soup.find_all('a', href=lambda x: x and '/produto/' in x)
if product_links:
    print(f"\n=== First product link ===")
    first = product_links[0]
    print(f"URL: {first.get('href')}")
    print(f"Classes: {first.get('class')}")
    print(f"Parent classes: {first.parent.get('class') if first.parent else 'None'}")
    print(f"Text: {first.get_text(strip=True)[:100]}")

from curl_cffi import requests
from bs4 import BeautifulSoup
from backend.services import utils as scrapers_utils
import re

def fetch_product(url):
    """
    Fetches product details from Amazon Brazil.
    Returns a dict with 'name', 'price', and 'url'.
    """
    try:
        # Use Chrome impersonation to bypass initial bot checks
        response = requests.get(
            url, 
            impersonate="chrome120", 
            headers=scrapers_utils.get_headers(),
            timeout=15,
            verify=False
        )
        
        if response.status_code not in [200, 201]:
            # Amazon 503 is often a captcha
            if response.status_code == 503:
                 return {"error": "Amazon CAPTCHA / 503 Service Unavailable", "url": url}
            return {"error": f"Status code {response.status_code}", "url": url}
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for CAPTCHA title
        if soup.title and ("CAPTCHA" in soup.title.string or "Robot Check" in soup.title.string):
            return {"error": "Amazon CAPTCHA triggered", "url": url}

        # 1. Product Name
        name_elem = soup.find(id="productTitle")
        name = name_elem.get_text(strip=True) if name_elem else None
        
        # 2. Price
        # Strategy: Look for the first visible price, usually .a-price .a-offscreen
        # The first one is typically the main buybox price
        price_elem = soup.select_one(".a-price .a-offscreen")
        price = 0.0
        
        if price_elem:
            price = scrapers_utils.clean_price(price_elem.get_text())
        
        # Fallback: Look for apex price if main one fails
        if not price:
            # Try finding price in hidden input if available (observed in debug logs)
            # <input type="hidden" name="items[0.base][customerVisiblePrice][displayString]" value="R$ 1.511,74" ...>
            hidden_input = soup.find("input", attrs={"name": re.compile(r"customerVisiblePrice")})
            if hidden_input:
                price = scrapers_utils.clean_price(hidden_input.get("value"))

        if name:
            return {
                "name": name,
                "price": price,
                "url": url,
                "store": "Amazon"
            }
            
        return {"error": "Could not extract Name/Price", "url": url}

    except Exception as e:
        return {"error": str(e), "url": url}

if __name__ == "__main__":
    test_url = "https://www.amazon.com.br/Processador-AMD-Ryzen-5-5600G/dp/B092L9GF5N/"
    print(fetch_product(test_url))

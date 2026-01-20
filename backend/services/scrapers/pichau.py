from curl_cffi import requests
from bs4 import BeautifulSoup
import json
import re
from backend.services import utils as scrapers_utils

def fetch_product(url):
    """
    Fetches product details from Pichau.
    Returns a dict with 'name', 'price', and 'url'.
    """
    try:
        # Use Chrome impersonation
        response = requests.get(
            url, 
            impersonate="chrome120", 
            headers=scrapers_utils.get_headers(),
            timeout=15,
            verify=False
        )
        
        if response.status_code not in [200, 201]:
            return {"error": f"Status code {response.status_code}", "url": url}
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Strategy: Meta Tags (Most robust for Pichau/Next.js RSC)
        # 1. Price
        price_meta = soup.find("meta", attrs={"name": "product:price:amount"})
        price_str = None
        if price_meta:
            price_str = price_meta.get("content")
        
        if not price_str:
            # Fallback to twitter:data1 which often holds price
            twitter_price = soup.find("meta", attrs={"name": "twitter:data1"})
            if twitter_price:
                 price_str = twitter_price.get("content")

        # 2. Name
        name_meta = soup.find("meta", property="og:title")
        name = None
        if name_meta:
            name = name_meta.get("content")
            # Cleanup: Remove " | Pichau" suffix if present
            if name:
                name = name.replace(" | Pichau", "").strip()
        
        if not name:
            # Fallback to H1
            h1 = soup.find("h1")
            if h1:
                name = h1.get_text(strip=True)

        # 3. Availability
        available = True
        avail_meta = soup.find("meta", attrs={"name": "product:availability"})
        if avail_meta:
            content = avail_meta.get("content", "").lower()
            if "out of stock" in content or "oos" in content or "out_of_stock" in content:
                available = False
        
        # Fallback: Check for "Esgotado" button or text
        if available:
            if soup.find(string=re.compile("Esgotado", re.IGNORECASE)) or soup.find(string=re.compile("Indisponível", re.IGNORECASE)):
                # Double check to ensure it's not "Not Esgotado" or something (unlikely)
                # Usually text "Esgotado" appears on the buy button.
                # Let's rely on price presence too.
                pass

        if name and price_str:
            return {
                "name": name,
                "price": scrapers_utils.clean_price(price_str),
                "url": url,
                "store": "Pichau",
                "available": available
            }
        
        # Fallback Strategy: If meta tags fail, try to find price in text (Risky)
        # Note: We rely on Meta tags for now as they proved present.
        
        return {
            "error": "Could not extract data (Meta tags missing)", 
            "url": url,
            "debug_name": name,
            "debug_price_raw": price_str
        }

    except Exception as e:
        return {"error": str(e), "url": url}

if __name__ == "__main__":
    test_url = "https://www.pichau.com.br/fonte-thermaltake-toughpower-sfx-850w-atx-3-1-full-modular-80-plus-platinum-preto-ps-stp-0850fnfapb-1"
    print(fetch_product(test_url))

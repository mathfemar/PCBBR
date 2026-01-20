import re

def get_headers():
    """
    Returns standard headers to mimic a real browser request.
    Useful if we need to customize headers further.
    """
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }

def clean_price(price_str):
    """
    Converts a price string (e.g., 'R$ 1.509,90', '1509.90') to a float.
    Returns None if conversion fails.
    """
    if not price_str:
        return None
    
    # Remove R$, spaces, etc.
    if isinstance(price_str, (float, int)):
        return float(price_str)
        
    clean_str = str(price_str).replace("R$", "").strip()
    
    # Handle Brazilian format (1.000,00) vs International (1,000.00)
    # Simple heuristic: if ',' is the last separator, it's decimal
    if "," in clean_str and "." in clean_str:
        if clean_str.rfind(",") > clean_str.rfind("."):
            # Brazilian: 1.500,00 -> remove dots, replace comma with dot
            clean_str = clean_str.replace(".", "").replace(",", ".")
        else:
            # International: 1,500.00 -> remove commas
            clean_str = clean_str.replace(",", "")
    elif "," in clean_str:
        # Assumed Brazilian decimal
        clean_str = clean_str.replace(",", ".")
        
    try:
        return float(clean_str)
    except ValueError:
        return None

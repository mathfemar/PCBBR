from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
import asyncio

# Import scrapers
from services.scrapers import amazon, kabum, pichau, terabyte

app = FastAPI(title="PCBBR API", version="1.0.0")

class ProductResult(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    url: str
    store: Optional[str] = None
    error: Optional[str] = None

# Import service
from services.product_service import save_product_history

@app.get("/")
def read_root():
    return {"message": "PCBBR API is running"}

@app.get("/search", response_model=List[ProductResult])
def search_product(url: str = Query(..., description="Product URL to scrape")):
    """
    Detects the store from the URL, runs the scraper, and saves to DB.
    """
    
    # Simple store detection logic
    if "amazon.com.br" in url:
        result = amazon.fetch_product(url)
    elif "kabum.com.br" in url:
        result = kabum.fetch_product(url)
    elif "pichau.com.br" in url:
        result = pichau.fetch_product(url)
    elif "terabyteshop.com.br" in url:
        result = terabyte.fetch_product(url)
    else:
        raise HTTPException(status_code=400, detail="Unsupported store or invalid URL")

    # Save to Database (Side Effect)
    try:
        if not result.get("error"):
            save_product_history(result)
    except Exception as e:
        print(f"DB Error: {e}")
        # We don't block the response if DB fails, but we log it.

    # Normalize result
    return [result]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

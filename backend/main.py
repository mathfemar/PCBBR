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

@app.get("/")
def read_root():
    return {"message": "PCBBR API is running"}

@app.get("/search", response_model=List[ProductResult])
async def search_product(url: str = Query(..., description="Product URL to scrape")):
    """
    Detects the store from the URL and runs the appropriate scraper.
    """
    
    # Simple store detection logic
    if "amazon.com.br" in url:
        # FastAPI handles async execution of synchronous functions in threadpool
        # But our scrapers are sync using requests/curl_cffi sync.
        # Ideally we should make scrapers async or use run_in_executor.
        # For now, just calling them directly (FastAPI puts them in threadpool).
        result = amazon.fetch_product(url)
    elif "kabum.com.br" in url:
        result = kabum.fetch_product(url)
    elif "pichau.com.br" in url:
        result = pichau.fetch_product(url)
    elif "terabyteshop.com.br" in url:
        result = terabyte.fetch_product(url)
    else:
        raise HTTPException(status_code=400, detail="Unsupported store or invalid URL")

    # Normalize result to list (for now just returning 1 item, but structure allows future expansion)
    # The scrapers return a dict. Adapter it to Pydantic.
    return [result]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

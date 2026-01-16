from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from pydantic import BaseModel
import asyncio

# Import scrapers
from services.scrapers import amazon, kabum, pichau, terabyte

app = FastAPI(title="PCBBR API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens em desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProductResult(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    url: str
    store: Optional[str] = None
    error: Optional[str] = None

# Import service
from services.product_service import save_product_history
from services import build_service, catalog_service

@app.get("/")
def read_root():
    return {"message": "PCBBR API is running"}

# ============ PRODUCT ENDPOINTS ============

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

# ============ BUILD ENDPOINTS ============

class CreateBuildRequest(BaseModel):
    name: str

class AddItemRequest(BaseModel):
    product_id: int
    category: str

@app.post("/builds")
def create_build(request: CreateBuildRequest):
    """Creates a new build"""
    try:
        build_id = build_service.create_build(request.name)
        return {"id": build_id, "name": request.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/builds")
def list_builds():
    """Lists all builds"""
    try:
        builds = build_service.list_builds()
        return builds
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/builds/{build_id}")
def get_build(build_id: int):
    """Gets a specific build with all items"""
    try:
        build = build_service.get_build(build_id)
        if not build:
            raise HTTPException(status_code=404, detail="Build not found")
        return build
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/builds/{build_id}/items")
def add_item_to_build(build_id: int, request: AddItemRequest):
    """Adds a product to a build"""
    try:
        build_service.add_item_to_build(build_id, request.product_id, request.category)
        return {"message": "Item added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/builds/{build_id}/items/{category}")
def remove_item_from_build(build_id: int, category: str):
    """Removes an item from a build by category"""
    try:
        build_service.remove_item_from_build(build_id, category)
        return {"message": "Item removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ CATALOG ENDPOINTS ============

@app.get("/catalog/search")
def search_catalog(
    query: str = Query(None, description="Search term"),
    category: str = Query(None, description="Filter by category"),
    store: str = Query(None, description="Filter by store"),
    limit: int = Query(20, description="Max results")
):
    """Searches the product catalog"""
    try:
        results = catalog_service.search_catalog(query, category, store, limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/catalog/update")
def update_catalog(
    category: str = Query(None, description="Update specific category"),
    store: str = Query(None, description="Update specific store")
):
    """Updates the product catalog (admin endpoint)"""
    try:
        if category:
            count = catalog_service.catalog_products_by_category(category, store)
            return {"message": f"Cataloged {count} products", "category": category}
        else:
            count = catalog_service.catalog_all_products()
            return {"message": f"Cataloged {count} products total"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{product_id}/price")
def fetch_product_price(product_id: int):
    """Fetches current price for a cataloged product"""
    try:
        # Get product from database
        from sqlmodel import Session
        from sqlalchemy import text
        from database import engine
        
        with Session(engine) as session:
            query = text("SELECT url FROM product WHERE id = :id")
            result = session.execute(query, {"id": product_id})
            row = result.fetchone()
            
            if not row:
                raise HTTPException(status_code=404, detail="Product not found")
            
            product_url = row[0]
        
        # Fetch price using existing scrapers
        if "amazon.com.br" in product_url:
            result = amazon.fetch_product(product_url)
        elif "kabum.com.br" in product_url:
            result = kabum.fetch_product(product_url)
        elif "pichau.com.br" in product_url:
            result = pichau.fetch_product(product_url)
        elif "terabyteshop.com.br" in product_url:
            result = terabyte.fetch_product(product_url)
        else:
            raise HTTPException(status_code=400, detail="Unsupported store")
        
        # Update price in database
        save_product_history(result)
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


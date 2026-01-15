from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(index=True, unique=True)
    store: str = Field(index=True)
    name: str = Field(index=True)
    current_price: float
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    price_history: List["PriceHistory"] = Relationship(back_populates="product")

class PriceHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    price: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    product: Product = Relationship(back_populates="price_history")

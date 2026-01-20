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
    category: Optional[str] = Field(default=None, index=True)  # CPU, GPU, RAM, etc
    image_url: Optional[str] = Field(default=None)
    available: bool = Field(default=True)

    # Relationships
    price_history: List["PriceHistory"] = Relationship(back_populates="product")
    build_items: List["BuildItem"] = Relationship(back_populates="product")

class PriceHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    price: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    product: Product = Relationship(back_populates="price_history")

class Build(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    items: List["BuildItem"] = Relationship(back_populates="build")

class BuildItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    build_id: int = Field(foreign_key="build.id")
    product_id: int = Field(foreign_key="product.id")
    category: str = Field(index=True)  # CPU, GPU, RAM, etc
    added_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    build: Build = Relationship(back_populates="items")
    product: Product = Relationship(back_populates="build_items")


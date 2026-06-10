from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    title: str
    price: float
    url: str
    supplier: Optional[str] = None
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    available: bool = True
    score: Optional[float] = None
    reason: Optional[str] = None
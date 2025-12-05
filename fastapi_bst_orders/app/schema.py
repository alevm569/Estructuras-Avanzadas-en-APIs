from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class ProductCreate(BaseModel):
    id: int = Field(..., gt=0)
    name: str
    price: float
    description: Optional[str] = None

class ProductOut(ProductCreate):
    pass

class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)

class OrderCreate(BaseModel):
    id: int = Field(..., gt=0)
    customer_name: str
    items: List[OrderItem]

class OrderOut(BaseModel):
    id: int
    customer_name: str
    items: List[Dict[str, Any]] 
    total: float
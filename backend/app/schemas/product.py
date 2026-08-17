from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    category_id: Optional[str] = None
    name: str
    sku: Optional[str] = None
    price: float
    tax_rate: Optional[float] = None
    modifiers: Optional[dict] = None
    barcode: Optional[str] = None
    is_active: bool = True
    stock_tracking: bool = False

class ProductOut(BaseModel):
    id: str
    name: str
    price: float
    tax_rate: Optional[float] = None

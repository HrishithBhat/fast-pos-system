from pydantic import BaseModel
from typing import List, Optional

class CartItem(BaseModel):
    product_id: str
    quantity: int
    modifiers: Optional[dict] = None
    discounts: Optional[list] = None

class PriceRequest(BaseModel):
    items: List[CartItem]

class PriceResponse(BaseModel):
    subtotal: float
    tax_total: float
    discount_total: float
    grand_total: float

class OrderCreate(BaseModel):
    items: List[CartItem]
    source: str = "pos"
    payment_method: str

class OrderOut(BaseModel):
    order_id: str
    status: str

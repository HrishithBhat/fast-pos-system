from sqlalchemy import Column, String, ForeignKey, Numeric, Integer, JSON
import uuid
from .base import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(String, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(String, ForeignKey("products.id", ondelete="SET NULL"))
    name_snapshot = Column(String, nullable=False)
    unit_price = Column(Numeric(12,2), nullable=False)
    quantity = Column(Integer, nullable=False)
    line_tax = Column(Numeric(12,2), nullable=False, default=0)
    line_discount = Column(Numeric(12,2), nullable=False, default=0)
    modifiers = Column(JSON, nullable=True)

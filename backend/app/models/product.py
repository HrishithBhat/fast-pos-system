from sqlalchemy import Column, String, Boolean, ForeignKey, Numeric, JSON
import uuid
from .base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(String, ForeignKey("categories.id", ondelete="SET NULL"))
    name = Column(String, nullable=False)
    sku = Column(String, nullable=True)
    price = Column(Numeric(12,2), nullable=False)
    tax_rate = Column(Numeric(5,2), nullable=True)
    modifiers = Column(JSON, nullable=True)
    barcode = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    stock_tracking = Column(Boolean, default=False)

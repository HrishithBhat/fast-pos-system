from sqlalchemy import Column, String, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.sql import func
import uuid
from .base import Base

class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(String, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    change = Column(Integer, nullable=False)
    reason = Column(String, nullable=False)
    order_id = Column(String, ForeignKey("orders.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

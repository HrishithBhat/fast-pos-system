from sqlalchemy import Column, String, ForeignKey, Numeric, TIMESTAMP
from sqlalchemy.sql import func
import uuid
from .base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    order_number = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    source = Column(String, nullable=False, default="pos")
    subtotal = Column(Numeric(12,2), nullable=False, default=0)
    tax_total = Column(Numeric(12,2), nullable=False, default=0)
    discount_total = Column(Numeric(12,2), nullable=False, default=0)
    grand_total = Column(Numeric(12,2), nullable=False, default=0)
    payment_status = Column(String, nullable=False, default="unpaid")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    completed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    cashier_id = Column(String, ForeignKey("users.id", ondelete="SET NULL"))

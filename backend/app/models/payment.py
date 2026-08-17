from sqlalchemy import Column, String, ForeignKey, Numeric, TIMESTAMP
from sqlalchemy.sql import func
import uuid
from .base import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(String, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    method = Column(String, nullable=False)
    amount = Column(Numeric(12,2), nullable=False)
    status = Column(String, nullable=False, default="pending")
    gateway_ref = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

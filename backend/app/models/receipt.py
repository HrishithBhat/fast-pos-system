from sqlalchemy import Column, ForeignKey, TIMESTAMP, Text, String
from sqlalchemy.sql import func
import uuid
from .base import Base

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(String, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    content_html = Column(Text, nullable=False)
    printed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

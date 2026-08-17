from sqlalchemy import Column, String, Integer, ForeignKey
import uuid
from .base import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    sort_order = Column(Integer, default=0)

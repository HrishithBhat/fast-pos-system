from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..core.deps import get_current_user
from ..models.base import get_session
from ..models.order import Order
from ..models.order_item import OrderItem
from ..schemas.order import OrderCreate, OrderOut
import uuid

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("", response_model=OrderOut)
async def create_order(data: OrderCreate, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    order = Order(tenant_id=user.tenant_id, order_number=str(uuid.uuid4())[:8], status="pending", source=data.source)
    session.add(order)
    await session.flush()
    for item in data.items:
        oi = OrderItem(tenant_id=user.tenant_id, order_id=order.id, product_id=uuid.uuid4(), name_snapshot="ITEM", unit_price=0, quantity=item.quantity)
        session.add(oi)
    await session.commit()
    return OrderOut(order_id=str(order.id), status=order.status)

@router.put("/{order_id}/status")
async def update_status(order_id: str, status: str, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Order).where(Order.id == uuid.UUID(order_id), Order.tenant_id == user.tenant_id))
    order = res.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    await session.commit()
    return {"status": order.status}

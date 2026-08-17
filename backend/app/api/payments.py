from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..core.deps import get_current_user
from ..models.base import get_session
from ..models.order import Order
from ..models.payment import Payment

router = APIRouter(prefix="/api/payments", tags=["payments"])

@router.post("/pay")
async def pay(order_id: str, method: str, amount: float, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Order).where(Order.id == order_id, Order.tenant_id == user.tenant_id))
    order = res.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    payment = Payment(tenant_id=user.tenant_id, order_id=order.id, method=method, amount=amount, status="succeeded")
    order.payment_status = "paid"
    session.add(payment)
    await session.commit()
    return {"status": payment.status}

@router.post("/refund")
async def refund(order_id: str, amount: float, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Order).where(Order.id == order_id, Order.tenant_id == user.tenant_id))
    order = res.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.payment_status = "refunded"
    await session.commit()
    return {"status": "refunded"}

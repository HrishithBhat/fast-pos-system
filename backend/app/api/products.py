from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..core.deps import get_current_user, require_roles
from ..models.base import get_session
from ..models.product import Product
from ..schemas.product import ProductCreate

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("")
async def list_products(user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Product).where(Product.tenant_id == user.tenant_id))
    products = res.scalars().all()
    return [{"id": str(p.id), "name": p.name, "price": float(p.price)} for p in products]

@router.post("", dependencies=[Depends(require_roles("admin", "manager"))])
async def create_product(data: ProductCreate, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    product = Product(tenant_id=user.tenant_id, name=data.name, sku=data.sku, price=data.price, tax_rate=data.tax_rate)
    session.add(product)
    await session.commit()
    return {"id": str(product.id)}

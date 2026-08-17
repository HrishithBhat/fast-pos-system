from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.base import get_session
from ..models.user import User
from ..models.tenant import Tenant
from ..schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from ..core.security import create_access_token, get_password_hash, verify_password
import uuid

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register")
async def register(data: RegisterRequest, session: AsyncSession = Depends(get_session)):
    # For simplicity in demo: use a demo tenant, create if missing
    res = await session.execute(select(Tenant).where(Tenant.code == "demo"))
    tenant = res.scalar_one_or_none()
    if not tenant:
        tenant = Tenant(name="Demo", code="demo")
        session.add(tenant)
        await session.flush()
        await session.commit()
    user = User(tenant_id=tenant.id, email=data.email, password_hash=get_password_hash(data.password), role=data.role)
    session.add(user)
    await session.commit()
    return {"id": str(user.id)}

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(User).where(User.email == data.email).order_by(User.created_at.desc()))
    user = res.scalars().first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "tenant_id": str(user.tenant_id), "role": user.role})
    return TokenResponse(access_token=token)

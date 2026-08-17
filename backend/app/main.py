import asyncio
from fastapi import FastAPI
from .core.config import settings
from .models.base import engine, Base
from .api import auth, products, orders, kds_ws, payments
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    # create tables for local dev (SQLite). For Postgres + Alembic, use migrations.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(kds_ws.router)

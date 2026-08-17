import pytest
from httpx import AsyncClient
from app.main import app
import asyncio
from app.models.base import engine, Base
from importlib import import_module
# ensure all models are registered without shadowing the FastAPI app symbol
import_module("app.models")

# Ensure tables exist before tests
async def _create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.get_event_loop().run_until_complete(_create_tables())

@pytest.mark.asyncio
async def test_create_order_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register & login
        await ac.post("/api/auth/register", json={"email": "o@r.com", "password": "pass", "role": "cashier"})
        resp = await ac.post("/api/auth/login", json={"email": "o@r.com", "password": "pass"})
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        # Create order (empty items demo)
        resp = await ac.post("/api/orders", headers=headers, json={"items": [], "payment_method": "cash", "source": "pos"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "pending"

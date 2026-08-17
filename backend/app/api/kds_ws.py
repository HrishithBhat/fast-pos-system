from fastapi import APIRouter, WebSocket

router = APIRouter(tags=["kds"])

@router.websocket("/ws/kds/{tenant_id}")
async def kds_ws(websocket: WebSocket, tenant_id: str):
    await websocket.accept()
    await websocket.send_json({"message": f"Connected to KDS for tenant {tenant_id}"})
    # Minimal demo; in production, store connection and broadcast order updates

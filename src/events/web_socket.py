import asyncio
from typing import Annotated

from fastapi import APIRouter, WebSocketDisconnect, WebSocket, Depends

from database.models import User
from events.dependencies import manager, get_admin_user_from_websocket

web_socket_router = APIRouter(prefix="/ws")


@web_socket_router.websocket("/event")
async def websocket_endpoint(
        websocket: WebSocket,
        user: Annotated[User, Depends(get_admin_user_from_websocket)]
):
    await manager.connect(websocket, admin_id=user.id)
    try:
        while True:
            await asyncio.sleep(4)
    except WebSocketDisconnect:
        manager.disconnect(user.id)

import asyncio

from fastapi import APIRouter, WebSocketDisconnect,WebSocket
from fastapi.params import Depends
from typing_extensions import Annotated

from auth.dependencies import get_admin_user
from database.models import User

web_socket_router = APIRouter(prefix="/ws/chat")


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket,  admin_id: int):

        await websocket.accept()
        if admin_id not in self.active_connections:
            self.active_connections[admin_id] = {}
        self.active_connections[admin_id].append(websocket)

    def disconnect(self, admin_id: int):
        if admin_id in self.active_connections :
            del self.active_connections[admin_id]
            if not self.active_connections[admin_id]:
                del self.active_connections[admin_id]

    async def send_personal_message(self, message: str, admin_id):
        if self.active_connections:
            for web_socket in self.active_connections[admin_id]:
                await web_socket.send_text(message)

manager=ConnectionManager()
@web_socket_router.websocket("/ws/{admin_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        user: Annotated[User, Depends(get_admin_user)]
):
    await manager.connect(websocket,admin_id=user.id)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        manager.disconnect(user.id)


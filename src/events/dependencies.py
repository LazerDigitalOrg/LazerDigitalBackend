from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.websockets import WebSocket, WebSocketDisconnect

from auth.services import AuthService
from database.models import User
from dependencies import get_async_session


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, admin_id: int):

        await websocket.accept()
        if admin_id not in self.active_connections:
            self.active_connections[admin_id] = []
        self.active_connections[admin_id].append(websocket)

    def disconnect(self, admin_id: int):
        if admin_id in self.active_connections:
            del self.active_connections[admin_id]

    async def send_personal_message(self, message: str, admin_id):

        if admin_id in self.active_connections:
            for websocket in self.active_connections[admin_id]:
                try:
                    await websocket.send_json(message)
                except WebSocketDisconnect:
                    self.disconnect(admin_id)


manager = ConnectionManager()


async def get_admin_user_from_websocket(
        websocket: WebSocket,
        session: Annotated[AsyncSession, Depends(get_async_session)],
) -> User:
    access_token = websocket.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missing"
        )
    refresh_token = websocket.cookies.get("refresh_token")
    auth_service = AuthService(session)
    payload = auth_service.token_manager.decode_jwt(access_token)
    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token"
        )
    user = await auth_service.get_user(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token: user not found"
        )
    expire = payload.get('exp')
    if not expire:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expiration not found"
        )
    if expire < datetime.now(timezone.utc).timestamp():
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No refresh token. Please login"
            )
        payload_refresh = auth_service.token_manager.decode_jwt(refresh_token)
        refresh_expire = payload_refresh.get('exp')

        if not refresh_expire:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expiration not found"
            )
        if refresh_expire < datetime.now(timezone.utc).timestamp():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token. Please login again"
            )
    return user

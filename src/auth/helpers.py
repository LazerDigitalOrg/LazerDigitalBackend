from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from auth.services import AuthService
from starlette import status
from fastapi import Request, Response
from datetime import datetime, timedelta, timezone
from typing import Annotated

from database.models import User
from dependencies import get_async_session

from fastapi import Depends
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"
async def get_access_token(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missing"
        )
    return access_token


async def get_refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is missing"
        )
    return refresh_token


async def get_new_access_token(
        refresh_token: str,
        response: Response):
    pass


async def get_current_user(
        access_token: Annotated[str, Depends(get_access_token)],
        refresh_token: Annotated[str, Depends(get_refresh_token)],
        session: Annotated[AsyncSession, Depends(get_async_session)],
        response: Response
) -> User | None:
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
        access_token = auth_service.token_manager.create_token({"sub": email}, ACCESS_TOKEN_TYPE)
        access_token_expires = datetime.now(timezone.utc) + timedelta(days=30)
        response.set_cookie(
            key="access_token", value=access_token, secure=True, httponly=True, samesite='none',
            expires=access_token_expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
        )

    return user


async def get_admin_user(
        user: Annotated[User, Depends(get_current_user)],
) -> User | None:
    if user.role == "admin":
        return user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User should be admin"
        )

    return None
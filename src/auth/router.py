from datetime import datetime, timezone, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, FastAPI, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from auth.schemas import TokenSchema, UserSchema, UserRole
from database.models import User
from src.auth.schemas import UserRegisterSchema, LoginSchema
from src.auth.services import AuthService
from dependencies import get_async_session
from auth.dependencies import get_current_user

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


async def generate_tokens(result: TokenSchema,
                          response: Response):
    access_token_expires = datetime.now(timezone.utc) + timedelta(days=30)
    refresh_token_expires = datetime.now(timezone.utc) + timedelta(days=30)

    response.set_cookie(
        key="access_token", value=result.access_token, secure=True, httponly=True, samesite='none',
        expires=access_token_expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
    )
    response.set_cookie(
        key="refresh_token", value=result.refresh_token, secure=True, httponly=True, samesite='none',
        expires=refresh_token_expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
    )


@auth_router.post("/register", response_model=UserRole)
async def register_user(
        session: Annotated[AsyncSession, Depends(get_async_session)],
        user: UserRegisterSchema,
        response: Response,
):
    auth_service = AuthService(session)
    result = await auth_service.add_user(user)
    tokens = result.get("tokens")
    await generate_tokens(tokens, response)
    return result.get("role")


@auth_router.post("/login", response_model=UserRole)
async def login_user(
        session: Annotated[AsyncSession, Depends(get_async_session)],
        user: LoginSchema,
        response: Response,

):
    auth_service = AuthService(session)
    result = await auth_service.login_user(user.email.__str__(), user.password)
    tokens = result.get("tokens")
    await generate_tokens(tokens, response)
    return result.get("role")


@auth_router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("refresh_token")
    response.delete_cookie("access_token")
    return {"result": "OK"}


@auth_router.get("/users/me/", response_model=UserSchema)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_user)],
):
    return UserSchema(
        email=current_user.email,
        phone_number=current_user.phone_number,
        username=current_user.username
    )


@auth_router.get("/users/events/")
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_user)],
):
    return []

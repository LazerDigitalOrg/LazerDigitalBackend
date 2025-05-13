from typing import Annotated, Union

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from dependencies import get_async_session, get_current_user, get_admin_user
from events.services import EventService

from events.schemas import (
    AllEventsResponse,
    CreateEventSchema,
    ActiveEventsResponse,
    ArchiveEventsResponse,
    ActiveEventDetailSchema,
    ArchiveEventDetailSchema,
    AdminActiveEventResponse
)

events_router = APIRouter(prefix="/events", tags=["Events"])


@events_router.get("/all", response_model=AllEventsResponse)
async def get_all_events(
        user: Annotated[User, Depends(get_admin_user)],
        session: AsyncSession = Depends(get_async_session),
        limit: int | None = 10,
        page: int | None = 1,
) -> AllEventsResponse:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User should be admin"
        )
    events_service = EventService(session)
    result = await events_service.get_events(limit=limit, page=page)
    return result


@events_router.get("/get_active", response_model=ActiveEventsResponse)
async def get_active_events(
        user: Annotated[User, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session),
) -> AllEventsResponse:
    events_service = EventService(session)
    result = await events_service.get_active_events(user.id)
    return result


@events_router.get("/get_archive", response_model=ArchiveEventsResponse)
async def get_active_events(
        user: Annotated[User, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session),
) -> AllEventsResponse:
    events_service = EventService(session)
    result = await events_service.get_archive_events(user.id)
    return result


@events_router.get("/get_active/{event_id}", response_model=Union[ActiveEventDetailSchema, AdminActiveEventResponse])
async def get_single_active_event(
        event_id: int,
        user: Annotated[User, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session),
) -> ActiveEventDetailSchema:
    events_service = EventService(session)
    result = await events_service.get_active_event(event_id)
    return result


@events_router.get("/get_archive/{event_id}", response_model=ArchiveEventDetailSchema)
async def get_single_archive_event(
        event_id: int,
        user: Annotated[User, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session),
) -> ActiveEventDetailSchema:
    events_service = EventService(session)
    result = await events_service.get_archive_event(event_id)
    return result


@events_router.post("/add")
async def create_event(
        new_event: CreateEventSchema,
        user: Annotated[User, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    event_session = EventService(session)
    result = await event_session.add_event(new_event, user.id)
    return {"detail": "OK", "event_id": result.id}

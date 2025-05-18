from typing import Annotated, Union

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, RoleEnum
from dependencies import get_async_session
from auth.dependencies import get_current_user, get_admin_user
from equipments.services import EquipmentService
from events.services import EventService

from events.schemas import (
    AllEventsResponse,
    CreateEventSchema,
    ActiveEventsResponse,
    ArchiveEventsResponse,
    ActiveEventDetailSchema,
    ArchiveEventDetailSchema,
    AdminActiveEventResponse,
    ConfirmEventSchema
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


@events_router.get("/active", response_model=ActiveEventsResponse)
async def get_active_events(
        user: Annotated[User, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session),
) -> AllEventsResponse:
    events_service = EventService(session)
    result = await events_service.get_active_events(user.id)
    return result


@events_router.get("/archive", response_model=ArchiveEventsResponse)
async def get_active_events(
        user: Annotated[User, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session),
) -> AllEventsResponse:
    events_service = EventService(session)
    result = await events_service.get_archive_events(user.id)
    return result


@events_router.get("/active/{event_id}", response_model=ActiveEventDetailSchema)
async def get_single_active_event(
        event_id: int,
        user: Annotated[User, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session),
) -> ActiveEventDetailSchema:
    events_service = EventService(session)
    result = await events_service.get_active_event(user_id=user.id, event_id=event_id)
    return result


@events_router.get("/admin/active/{event_id}", response_model=AdminActiveEventResponse)
async def get_single_active_event(
        event_id: int,
        user: Annotated[User, Depends(get_admin_user)],
        session: AsyncSession = Depends(get_async_session),
) -> ActiveEventDetailSchema:
    events_service = EventService(session)
    result = await events_service.get_admin_active_event(event_id)
    return result


@events_router.post("/admin/confirm_event/{event_id}")
async def get_single_active_event(
        event: ConfirmEventSchema,
        user: Annotated[User, Depends(get_admin_user)],
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    events_service = EventService(session)
    result = await events_service.confirm_event(event)
    return result


@events_router.get("/archive/{event_id}", response_model=ArchiveEventDetailSchema)
async def get_single_archive_event(
        event_id: int,
        user: Annotated[User, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session),
) -> ActiveEventDetailSchema:
    events_service = EventService(session)
    result = await events_service.get_archive_event(event_id, user)

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
    return {"result": "OK", "event_id": result.id}

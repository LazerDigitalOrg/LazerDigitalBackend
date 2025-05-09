from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.helpers import get_admin_user, get_current_user
from database.models import User
from dependencies import get_async_session
from events.schemas import AllEventsSchema, AllEventsResponse, CreateEventSchema
from events.services import EventService

events_router = APIRouter(prefix="/events", tags=["Events"])


@events_router.get("/all", response_model=AllEventsResponse)
async def get_all_events(
        user: Annotated[User, Depends(get_admin_user)],
        session: AsyncSession = Depends(get_async_session),
        limit: int | None = 1,
        page: int | None = 10,
) -> AllEventsResponse:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User should be admin"
        )
    events_service = EventService(session)
    result = await events_service.get_events(limit=limit, page=page)
    return result


@events_router.post("/add")
async def create_event(
        new_event: CreateEventSchema,
        user: Annotated[User, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session),
)->dict:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    event_session = EventService(session)
    result = await event_session.add_event(new_event, user.id)
    return {"detail": "OK", "event_id": result.id}

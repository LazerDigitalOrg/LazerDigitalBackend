from database.models import EventStatusEnum, Event
from events.repositories import EventRepository
from events.schemas import (
    AllEventsResponse,
    AllEventsSchema,
    CreateEventSchema,
    ActiveEventsResponse,
    ActiveEventSchema, ArchiveEventSchema, ArchiveEventsResponse,
)


class EventService:

    def __init__(self, session):
        self.event_repository = EventRepository(session)

    async def get_events(
            self, limit: int, page: int,
    ) -> AllEventsResponse:
        if page < 1:
            page = 1
        offset = (page - 1) * limit
        events = await self.event_repository.get_all_events(
            limit, offset
        )

        events = [
            AllEventsSchema(
                title=event.title,
                date=event.formatted_period,
            )
            for event in events
        ]

        return AllEventsResponse(events=events, offset=offset, totalCount=len(events))

    async def add_event(self, new_event: CreateEventSchema, user_id: int):
        return await self.event_repository.add(new_event, user_id)

    async def get_active_events(self):
        events = await self.event_repository.get_events_by_condition(Event.status == EventStatusEnum.ACTIVE)
        events = [
            ActiveEventSchema(
                title=event.title,
                date=event.formatted_period,
                estimate=event.estimate
            )
            for event in events
        ]
        return ActiveEventsResponse(events=events)

    async def get_archive_events(self):
        events = await self.event_repository.get_events_by_condition(Event.status == EventStatusEnum.ARCHIVE)
        events = [
            ArchiveEventSchema(
                title=event.title,
                date=event.formatted_period,
                equipment_count=event.equipment_count,
                estimate=event.estimate
            )
            for event in events
        ]
        return ArchiveEventsResponse(events=events)

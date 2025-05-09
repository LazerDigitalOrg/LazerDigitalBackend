from database.models import EventStatusEnum
from events.repositories import EventRepository
from events.schemas import AllEventsResponse, AllEventsSchema, CreateEventSchema


class EventService:

    def __init__(self, session):
        self.event_repository = EventRepository(session)

    async def get_events(
            self, limit: int, page: int,
    ) -> AllEventsResponse :
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

        return AllEventsResponse(events=events,offset=offset,totalCount=len(events))

    async def add_event(self, new_event:CreateEventSchema, user_id:int):
        return await self.event_repository.add(new_event, user_id)


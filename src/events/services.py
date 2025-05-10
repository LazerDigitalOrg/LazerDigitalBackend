from fastapi import HTTPException, status

from auth.repositories import UserRepository
from database.models import EventStatusEnum, Event, RoleEnum
from events.repositories import EventRepository
from events.schemas import (
    AllEventsResponse,
    AllEventsSchema,
    CreateEventSchema,
    ActiveEventsResponse,
    ActiveEventSchema, ArchiveEventSchema, ArchiveEventsResponse,
    ActiveEventDetailSchema, ArchiveEventDetailSchema,
)


class EventService:

    def __init__(self, session):
        self.event_repository = EventRepository(session)
        self.user_repository = UserRepository(session)

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
        manager = await self.user_repository.get_user_by_role(RoleEnum.MANAGER)
        lightning_designer = await self.user_repository.get_user_by_role(RoleEnum.LIGHTNING_DESIGNER)
        return await self.event_repository.add(new_event, user_id, manager.id, lightning_designer.id)

    async def get_active_events(self, user_id):
        events = await self.event_repository.get_events_by_condition(
            Event.status == EventStatusEnum.ACTIVE,
            Event.customer_id == user_id
        )
        events = [
            ActiveEventSchema(
                title=event.title,
                event_id=event.id,
                date=event.formatted_period,
                estimate=event.estimate
            )
            for event in events
        ]
        return ActiveEventsResponse(events=events)

    async def get_archive_events(self, user_id):
        events = await self.event_repository.get_events_by_condition(
            Event.status == EventStatusEnum.ARCHIVE,
            Event.customer_id == user_id
        )
        events = [
            ArchiveEventSchema(
                title=event.title,
                date=event.formatted_period,
                event_id=event.id,
                equipment_count=event.equipment_count,
                estimate=event.estimate
            )
            for event in events
        ]
        return ArchiveEventsResponse(events=events)

    async def get_event(self, event_id):
        pass

    async def get_active_event(self, event_id):
        event = await self.event_repository.get_single_event(event_id=event_id)
        event = event[0]
        if event.status != EventStatusEnum.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event is not active"
            )
        equipments = [
            f"{event_equipment.quantity} X {event_equipment.equipment.title}"
            for event_equipment in event.equipments
        ] if event.equipments else []

        return ActiveEventDetailSchema(
            event_date=event.event_date,
            event_end_date=event.event_end_date,
            title=event.title,
            type=event.type,
            area_plan=event.area_plan,
            address=event.address,
            payment_method=event.payment_method,
            comment=event.comment,
            site_area=event.site_area,
            ceiling_height=event.ceiling_height,
            has_tv=event.has_tv,
            min_install_time=event.min_install_time,
            total_power=event.total_power,
            has_downtime=event.has_downtime,
            manager_name=event.manager.username,
            manager_phone_number=event.manager.phone_number,
            equipment=equipments,
            estimate=event.estimate,
            estimate_xlsx=event.estimate_xlsx,
            discount=event.discount
        )

    async def get_archive_event(self, event_id):
        event = await self.event_repository.get_single_event(event_id=event_id)
        event = event[0]
        if event.status != EventStatusEnum.ARCHIVE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event is not archive"
            )
        equipment_count = 0
        equipments = []
        if event.equipments:
            for event_equipment in event.equipments:
                equipments.append(f"{event_equipment.quantity} X {event_equipment.equipment.title}")
                equipment_count+=event_equipment.quantity

        return ArchiveEventDetailSchema(
            event_date=event.event_date,
            title=event.title,
            address=event.address,
            total_power=event.total_power,
            equipment_count=equipment_count,
            equipment=equipments,
            lighting_designer=event.lightning_designer.username,
            total_sum=event.estimate * (1 - event.discount)
        )

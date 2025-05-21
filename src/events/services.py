from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.repositories import UserRepository
from database.models import EventStatusEnum, Event, RoleEnum, User, Equipment, EventEquipment
from equipments.repositories import EquipmentRepository, CategoryRepository, EventEquipmentRepository
from events.repositories import EventRepository
from events.schemas import (
    AllEventsResponse,
    AllEventsSchema,
    CreateEventSchema,
    ActiveEventsResponse,
    ActiveEventSchema,
    ArchiveEventSchema,
    ArchiveEventsResponse,
    ActiveEventDetailSchema,
    ArchiveEventDetailSchema,
    AdminActiveEventResponse, ConfirmEventSchema

)


class EventService:

    def __init__(self, session):
        self.event_repository = EventRepository(session)
        self.user_repository = UserRepository(session)
        self.category_repository = CategoryRepository(session)
        self.equipment_repository = EquipmentRepository(session)
        self.event_equipment_repository = EventEquipmentRepository(session)
        self.session: AsyncSession = session

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
                status=event.status,
                event_id=event.id
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
                estimate=event.estimate if event.estimate else 0
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

    async def get_active_event(self, user_id, event_id):
        event = await self.event_repository.get_single_event_by_condition(
            Event.customer_id == user_id,
            Event.id == event_id
        )
        if( event == None):
            return None
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
            estimate=event.estimate if event.estimate else 0,
            estimate_xlsx=event.estimate_xlsx,
            discount=event.discount if event.estimate else 0,
        )

    async def get_archive_event(self, event_id, user: User):
        if user.role == RoleEnum.USER:
            event = await self.event_repository.get_single_event_by_condition(
                Event.customer_id == user.id,
                Event.id == event_id
            )
        else:
            event = await self.event_repository.get_single_event_by_condition(Event.id == event_id)
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
                equipment_count += event_equipment.quantity

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

    async def get_admin_active_event(self, event_id):
        event = await self.event_repository.get_single_event_by_condition(Event.id == event_id)
        if event == None :
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event is not exists"
            )
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

        discount = event.discount if event.discount else 0
        estimate = event.estimate if event.estimate else 0

        return AdminActiveEventResponse(
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
            equipments=equipments,
            estimate=estimate,
            discount=discount,
        )

    async def confirm_event(self, event: ConfirmEventSchema):
        existing_event: tuple = await self.event_repository.get_single_event_by_condition(
            Event.id == event.event_id,
            with_for_update=True
        )
        if not existing_event:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Event does not exists"
            )
        existing_event = existing_event[0]
        print(event.discount)
        price = 0
        for equipment in event.equipments:
            print(equipment.title)
            title = equipment.title
            quantity = equipment.quantity
            existing_equipment: Equipment = await self.equipment_repository.get_single_equipment_by_condition(
                Equipment.title == title,
                with_for_update=True
            )
            if not existing_equipment:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Equipment {title} does not exists"
                )
            if quantity <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Quantity of {title} can't be less then 0"
                )

            existing_event_equipment = await self.event_equipment_repository.get_event_equipment_by_condition(
                EventEquipment.event_id == existing_event.id,
                EventEquipment.equipment_id == existing_equipment.id,
                with_for_update=True
            )
            if existing_event_equipment:
                if (existing_equipment.quantity + existing_event_equipment.quantity < quantity):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Quantity of this equipment - {equipment.title} is less than available : {existing_equipment.quantity + existing_event_equipment.quantity}"
                    )
                existing_equipment.quantity = existing_event_equipment.quantity + existing_equipment.quantity - quantity
                existing_event_equipment.quantity = quantity
            else:
                event_equipment = EventEquipment(
                    equipment_id=existing_equipment.id,
                    event_id=existing_event.id,
                    quantity=quantity
                )
                if (existing_equipment.quantity < quantity):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Quantity of this equipment - {equipment.title} is less than available : {existing_equipment.quantity}"
                    )
                existing_equipment.quantity -= quantity
                self.session.add(event_equipment)
            price += existing_equipment.rental_price * quantity
            await self.session.commit()

        existing_event.estimate = price * (1 - event.discount / 100)
        existing_event.discount = event.discount

        await self.session.commit()

        return {"result": "OK"}

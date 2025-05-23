from sqlalchemy import select, insert, and_
from sqlalchemy.orm import joinedload, selectinload

from database.models import Event, EventStatusEnum, EventEquipment, Equipment
from events.schemas import CreateEventSchema


class EventRepository:
    def __init__(self, session):
        self.session = session

    async def get_all_events(self, limit, offset):
        stmt = (select(Event)
                .limit(limit)
                .offset(offset)
                .order_by(Event.created_at.desc()))

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add(self, new_event: CreateEventSchema, user, manager, lightning_designer):
        event = Event(
            event_date=new_event.event_date,
            event_end_date=new_event.event_end_date,
            title=new_event.title,
            type=new_event.type,
            status=EventStatusEnum.ACTIVE,
            area_plan=new_event.area_plan,
            address=new_event.address,
            payment_method=new_event.payment_method,
            comment=new_event.comment,
            site_area=new_event.site_area,
            ceiling_height=new_event.ceiling_height,
            has_tv=new_event.has_tv,
            min_install_time=new_event.min_install_time,
            total_power=new_event.total_power,
            has_downtime=new_event.has_downtime,
            customer_id=user.id,
            manager_id=manager.id,
            lightning_designer_id=lightning_designer.id
        )
        self.session.add(event)

        await self.session.commit()
        await self.session.refresh(event)
        await self.session.refresh(user)
        await self.session.refresh(manager)
        await self.session.refresh(lightning_designer)


        return event

    async def get_events_by_condition(self, *predicate):
        stmt = (
            select(Event).
            where(*predicate).
            order_by(Event.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_single_event_by_condition(self, *predicate, with_for_update=False):
        stmt = (
            select(Event)
            .options(
                selectinload(Event.equipments).options(joinedload(EventEquipment.equipment))
                , joinedload(Event.manager), joinedload(Event.lightning_designer)

            ).where(*predicate)
        )
        if with_for_update:
            stmt = stmt.with_for_update(of=Event)

        result = await self.session.execute(stmt)
        event = result.unique().one_or_none()
        return event

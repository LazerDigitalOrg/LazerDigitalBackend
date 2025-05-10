from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, field_validator, validator

from database.models import EventTypeEnum, EventStatusEnum, PaymentMethod


class AllEventsSchema(BaseModel):
    title: str
    date: str


class AllEventsResponse(BaseModel):
    totalCount: int
    offset: int
    events: List[AllEventsSchema]


class ActiveEventSchema(BaseModel):
    title: str
    date: str
    estimate: float | None


class ArchiveEventSchema(BaseModel):
    title: str
    date: str
    equipment_count: int | None
    estimate: float | None


class ActiveEventsResponse(BaseModel):
    events: List[ActiveEventSchema]


class ArchiveEventsResponse(BaseModel):
    events: List[ArchiveEventSchema]


class CreateEventSchema(BaseModel):
    event_date: datetime
    event_end_date: datetime
    title: str
    type: EventTypeEnum
    area_plan: bytes | None
    address: str
    payment_method: PaymentMethod
    comment: str | None
    site_area: float | None
    ceiling_height: float | None
    has_tv: bool
    min_install_time: int
    total_power: int | None
    has_downtime: bool
    estimate: int | None

    @field_validator("event_date", "event_end_date")
    def parse_datetime_start(cls, value: str) -> datetime:
        if isinstance(value, datetime):
            return value
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M")
        except ValueError:
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                raise ValueError(
                    "Неверный формат даты. Ожидается 'YYYY-MM-DD HH:MM' или ISO 8601 ('YYYY-MM-DDTHH:MM:SS')"
                )

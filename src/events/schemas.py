from datetime import datetime, timezone
from typing import List

from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator, validator
from typing_extensions import Annotated

from database.models import EventTypeEnum, EventStatusEnum, PaymentMethod


class AllEventsSchema(BaseModel):
    title: str
    date: str
    event_id: int
    status: EventStatusEnum


class AllEventsResponse(BaseModel):
    totalCount: int
    offset: int
    events: List[AllEventsSchema]


class ActiveEventSchema(BaseModel):
    title: str
    event_id: int
    date: str
    estimate: float | None


class ArchiveEventSchema(BaseModel):
    title: str
    event_id: int
    date: str
    equipment_count: int | None
    estimate: float | None


class EventDetailBaseSchema(BaseModel):
    @field_validator("event_date", "event_end_date", check_fields=False)
    def parse_datetime_start(cls, value: datetime) -> str:
        if isinstance(value, str):
            return value
        try:
            return value.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            return str(value)


class EquipmentTitleSchema(BaseModel):
    title: str


class EquipmentCategorySchema(BaseModel):
    category_title: str
    equipments_catalog: List[EquipmentTitleSchema]


class EquipmentQuantitySchema(BaseModel):
    title: str
    quantity: int


class AdminActiveEventResponse(EventDetailBaseSchema):
    event_date: datetime | str
    event_end_date: datetime | str
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
    estimate: float
    discount: float
    equipments: List[str]

class ConfirmEventEquipmentsSchema(BaseModel):
    title: str
    quantity: int

class ConfirmEventSchema(BaseModel):
    event_id: int
    discount: float
    equipments: List[ConfirmEventEquipmentsSchema]

    @field_validator("discount")
    def check_discount(cls, value: float) -> float:
        if (value < 0 or value >= 100):
            raise ValueError("Discount can't be less then 0 or more then 100")
        return value


class ArchiveEventDetailSchema(EventDetailBaseSchema):
    event_date: str | datetime
    title: str
    address: str
    total_power: int
    lighting_designer: str
    equipment: List[str]
    equipment_count: int
    total_sum: float


class ActiveEventDetailSchema(EventDetailBaseSchema):
    event_date: str | datetime
    event_end_date: str | datetime
    title: str
    type: EventTypeEnum
    area_plan: bytes | None
    address: str
    payment_method: PaymentMethod
    comment: str | None
    site_area: int | None
    ceiling_height: float | None
    has_tv: bool
    min_install_time: int
    total_power: int | None
    has_downtime: bool
    manager_name: str
    manager_phone_number: str
    equipment: List[str]
    estimate: float | None
    estimate_xlsx: bytes | None
    discount: float | None


class ActiveEventsResponse(BaseModel):
    events: List[ActiveEventSchema]


class ArchiveEventsResponse(BaseModel):
    events: List[ArchiveEventSchema]


class CreateEventSchema(BaseModel):
    event_date: datetime | str
    event_end_date: datetime | str
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

    @field_validator("event_date", "event_end_date")
    def parse_datetime_start(cls, value: str) -> datetime:
        if isinstance(value, datetime):
            return value
        try:
            date = datetime.strptime(value, "%Y-%m-%d %H:%M")
            print("no")
            if date.timestamp() < datetime.now(timezone.utc).timestamp():
                print("yes")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Дата мероприятия не может быть меньше чем сегодняшний день"
                )
            return date
        except ValueError:
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                raise ValueError(
                    "Неверный формат даты. Ожидается 'YYYY-MM-DD HH:MM' или ISO 8601 ('YYYY-MM-DDTHH:MM:SS')"
                )



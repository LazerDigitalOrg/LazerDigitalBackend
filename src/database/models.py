from enum import StrEnum
from typing import List
from src.utils import format_event_dates
from sqlalchemy import (
    String,
    DateTime,
    Text,
    func,
    ForeignKey,
    Integer,
    JSON,
    LargeBinary,

    Enum as SQLAlchemyEnum, Float, Boolean
)

from src.database.database import async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, index=True)


class RoleEnum(StrEnum):
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"
    LIGHTNING_DESIGNER="lightning_designer"


class EventTypeEnum(StrEnum):
    WEDDING = "Свадьба"
    CORPORATIVE = "Корпоратив"
    CONCERT = "Концерт"
    BIRTHDAY = "День рождения"


class EventStatusEnum(StrEnum):
    ACTIVE = "ACTIVE"
    ARCHIVE = "ARCHIVE"
    PAID = "PAID"


class PaymentMethod(StrEnum):
    EP = "ИП"
    LLL = "ООО"
    INDIVIDUAL = "Физ. лицо"


class RefreshToken(Base):
    __tablename__ = "refreshtoken"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    expired_id: Mapped[DateTime] = mapped_column(DateTime)
    refresh_token: Mapped[str] = mapped_column(String)
    isValid: Mapped[bool] = mapped_column(Boolean)


class Event(Base):
    __tablename__ = "events"
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    event_date: Mapped[DateTime] = mapped_column(DateTime)
    event_end_date: Mapped[DateTime] = mapped_column(DateTime)
    title: Mapped[String] = mapped_column(String)
    type: Mapped[EventTypeEnum] = mapped_column(SQLAlchemyEnum(EventTypeEnum, name='event_type_enum'))
    status: Mapped[EventStatusEnum] = mapped_column(SQLAlchemyEnum(EventStatusEnum, name='event_status_enum'),
                                                    default=EventStatusEnum.ACTIVE)
    area_plan: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    estimate_xlsx: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    address: Mapped[str] = mapped_column(String)
    payment_method: Mapped[PaymentMethod] = mapped_column(SQLAlchemyEnum(PaymentMethod, name='payment_method_enum'))
    comment: Mapped[String] = mapped_column(Text, nullable=True)
    site_area: Mapped[int] = mapped_column(Integer, nullable=True)
    ceiling_height: Mapped[float] = mapped_column(Float, nullable=True)
    has_tv: Mapped[bool] = mapped_column(Boolean)
    min_install_time: Mapped[int] = mapped_column(Integer)
    total_power: Mapped[int] = mapped_column(Integer, nullable=True)
    has_downtime: Mapped[bool] = mapped_column(Boolean)
    estimate: Mapped[float] = mapped_column(Float, nullable=True)
    discount: Mapped[float] = mapped_column(Float, nullable=True)
    total_sum:Mapped[float] = mapped_column(Float, nullable=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    customer: Mapped["User"] = relationship(back_populates="events", foreign_keys=[customer_id])
    manager_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    manager: Mapped["User"] = relationship(back_populates="managed_events", foreign_keys=[manager_id])
    lightning_designer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    lightning_designer: Mapped["User"] = relationship(back_populates="lightning_events", foreign_keys=[lightning_designer_id])
    equipments: Mapped[List["EventEquipment"]] = relationship()
    equipment_count: Mapped[int] = mapped_column(Integer, nullable=True)

    @property
    def formatted_period(self):
        return format_event_dates(self.event_date, self.event_end_date)



class Role(Base):
    __tablename__ = "roles"
    title: Mapped[RoleEnum] = mapped_column(SQLAlchemyEnum(RoleEnum), unique=True)


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String(12))
    avatar_url: Mapped[str] = mapped_column(String, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    role: Mapped[RoleEnum] = mapped_column(ForeignKey("roles.title"), nullable=False)
    person_position: Mapped[str] = mapped_column(String, nullable=True)
    events: Mapped[List["Event"]] = relationship(back_populates="customer", foreign_keys="[Event.customer_id]")
    managed_events: Mapped[List["Event"]] = relationship(back_populates="manager", foreign_keys="[Event.manager_id]")
    lightning_events: Mapped[List["Event"]] = relationship(back_populates="lightning_designer", foreign_keys="[Event.lightning_designer_id]")


class Reviews(Base):
    __tablename__ = "reviews"
    review_title: Mapped[str] = mapped_column(String)
    review_description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Category(Base):
    __tablename__ = "categories"
    title: Mapped[str] = mapped_column(String)
    category_slug: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    hint: Mapped[str] = mapped_column(Text)
    photo_url: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    parent_category_slug: Mapped[str] = mapped_column(ForeignKey("categories.category_slug"), nullable=True)


class Brand(Base):
    __tablename__ = "brands"
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)


class Equipment(Base):
    __tablename__ = "equipments"
    title: Mapped[str] = mapped_column(String,unique=True)
    rental_price: Mapped[int] = mapped_column(Integer, nullable=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship()
    category_slug: Mapped[str] = mapped_column(String)
    equipment_slug: Mapped[str] = mapped_column(String, nullable=True, unique=True)
    power: Mapped[int] = mapped_column(String, nullable=True)
    total_power: Mapped[int] = mapped_column(String, nullable=True)
    producer: Mapped[str] = mapped_column(String, nullable=True)
    characteristics: Mapped[dict] = mapped_column(JSON, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    weight: Mapped[int] = mapped_column(Integer)
    available_quantity: Mapped[int] = mapped_column(Integer)
    photo_url: Mapped[str] = mapped_column(String, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer)


class EventEquipment(Base):
    __tablename__ = "eventequipments"
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipments.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    equipment: Mapped["Equipment"] = relationship()
    event: Mapped["Event"] = relationship()



class Employee(Base):
    __tablename__ = "employees"
    employee_first_name: Mapped[str] = mapped_column(String)
    employee_last_name: Mapped[str] = mapped_column(String)
    gender: Mapped[str] = mapped_column(String)
    date_of_birth: Mapped[DateTime] = mapped_column(DateTime)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=True)


class Position(Base):
    __tablename__ = "positions"
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)


class PositionEmployee(Base):
    __tablename__ = "positionemployees"
    hiring_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    salary: Mapped[int] = mapped_column(Integer)
    position_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    employee_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)


class Services(Base):
    __tablename__ = "services"
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)


class Orders(Base):
    __tablename__ = "orders"
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    total_sum: Mapped[int] = mapped_column(Integer)
    created_At: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


from sqlalchemy.ext.asyncio import AsyncEngine


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_tables(async_engine))

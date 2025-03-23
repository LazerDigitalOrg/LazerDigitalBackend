from sqlalchemy import String, DateTime, Text, func, ForeignKey, Integer, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from src.database.database import async_engine
from sqlalchemy import String, DateTime, Text, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

class Role(Base):
    __tablename__ = "roles"
    title: Mapped[str] = mapped_column(String)



class User(Base):
    __tablename__ = "users"
    user_last_name: Mapped[str] = mapped_column(String)
    user_first_name: Mapped[str] = mapped_column(String)
    user_middle_name: Mapped[str] = mapped_column(String, nullable=True)
    user_phone_number: Mapped[str] = mapped_column(String(12))
    avatar_url: Mapped[str] = mapped_column(String, nullable=True)
    user_email_address: Mapped[str] = mapped_column(String, unique=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)

    person_position: Mapped[str] = mapped_column(String, nullable=True)
class Reviews(Base):
    __tablename__ = "reviews"
    review_title: Mapped[str] = mapped_column(String)
    review_description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Events(Base):
    __tablename__ = "events"
    status: Mapped[str] = mapped_column(String)
    total_power: Mapped[int] = mapped_column(Integer)
    total_sum: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    event_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Category(Base):
    __tablename__ = "categories"
    title: Mapped[str] = mapped_column(String)
    category_slug: Mapped[str] = mapped_column(String,unique=True,nullable=True)
    hint: Mapped[str] = mapped_column(Text)
    photo_url: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(Text)


class Brand(Base):
    __tablename__ = "brands"
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)


class Equipment(Base):
    __tablename__ = "equipments"
    title: Mapped[str] = mapped_column(String)
    rental_price: Mapped[int] = mapped_column(Integer)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category_slug: Mapped[str] = mapped_column(String)
    equipment_slug: Mapped[str] = mapped_column(String, nullable=True, unique=True)
    power: Mapped[int] = mapped_column(String, nullable=True)
    total_power: Mapped[int] = mapped_column(String, nullable=True)
    producer: Mapped[str] = mapped_column(String)
    characteristics: Mapped[dict] = mapped_column(JSON)
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
    # Импортируем модели, чтобы они зарегистривались в Base.metadata
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
import asyncio
asyncio.run(create_tables(async_engine))


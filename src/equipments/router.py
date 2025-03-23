from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.equipments.schemas import EquipmentSchema, CategorySchema, CategoryResponse, EquipmentResponse
from src.equipments.services import EquipmentService, CategoryService
from dependencies import get_async_session

equipments_router = APIRouter(prefix="/store", tags=["store"])


@equipments_router.get("/{category_slug}/{equipment_slug}", response_model=EquipmentSchema)
async def get_equipment_by_equipment_slu(
        session: Annotated[AsyncSession, Depends(get_async_session)],
        category_slug:str,
        equipment_slug:str
):
    equipment_service = EquipmentService(session)
    return await equipment_service.get_single_equipment(equipment_slug)


@equipments_router.get("/{category_slug}", response_model=EquipmentResponse)
async def get_equipments_by_catgory(
        session: Annotated[AsyncSession, Depends(get_async_session)],
        category_slug: str,
        limit: int = 10,
        page: int = 1,
):
    equipment_service = EquipmentService(session)
    return await equipment_service.get_equipments_by_category(limit, page, category_slug)


@equipments_router.get("", response_model=CategoryResponse)
async def get_categories(
        session: Annotated[AsyncSession, Depends(get_async_session)],
):
    category_service = CategoryService(session)
    return await category_service.get_categories()

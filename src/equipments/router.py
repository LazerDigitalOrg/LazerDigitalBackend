from typing import Annotated, Optional, Union

from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import status
from src.equipments.schemas import EquipmentSchema, CategorySchema, CategoryResponse, EquipmentResponse
from src.equipments.services import EquipmentService, CategoryService
from dependencies import get_async_session

equipments_router = APIRouter(prefix="/store", tags=["Store"])


@equipments_router.get("/{category_slug}/{path:path}", response_model=Optional[Union[EquipmentResponse, EquipmentSchema]])
async def get_equipment_or_equipments(
        session: Annotated[AsyncSession, Depends(get_async_session)],
        category_slug,
        path: str,
        limit: int | None = 10,
        page: int | None = 1,
):

    equipment_service = EquipmentService(session)
    category_service = CategoryService(session)

    path = path.split("/")
    if len(path) == 2:
        return await equipment_service.get_single_equipment(path[1],category_slug+"/"+path[0])
    if len(path) == 1:
        if await category_service.is_category(category_slug+"/"+path[0]):

            equipments = await equipment_service.get_equipments_by_category(limit, page,category_slug+"/"+path[0])
            return equipments
        else:
            return await equipment_service.get_single_equipment(path[0],category_slug)


@equipments_router.get("/{category_slug}", response_model=Union[EquipmentResponse, CategoryResponse])
async def get_equipments_or_categories(
        session: Annotated[AsyncSession, Depends(get_async_session)],
        category_slug: str,
        limit: int | None = 10,
        page: int | None = 1,
):
    category_service = CategoryService(session)
    equipment_service = EquipmentService(session)
    result = await category_service.get_child_categories(category_slug)
    if result is None:
        return await equipment_service.get_equipments_by_category(limit, page, category_slug)
    return result


@equipments_router.get("", response_model=CategoryResponse)
async def get_categories(
        session: Annotated[AsyncSession, Depends(get_async_session)],
):
    category_service = CategoryService(session)
    return await category_service.get_categories()

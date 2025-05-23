from typing import Annotated, Optional, Union
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from src.equipments.schemas import EquipmentSchema, CategoryResponse, EquipmentResponse, EventEquipmentCategorySchema
from src.equipments.services import EquipmentService, CategoryService
from dependencies import get_async_session, get_redis

equipments_router = APIRouter(prefix="/store", tags=["Store"])


@equipments_router.get("/events/equipments-by-category")
async def get_event_equipments(
        session: Annotated[AsyncSession, Depends(get_async_session)],
        redis_client: Annotated[Redis, Depends(get_redis)]
):
    if cached := await redis_client.get("equipments-by-category"):
        return json.loads(cached)
    equipment_service = EquipmentService(session)
    result = await equipment_service.get_event_equipments()
    await redis_client.set(
        "equipments-by-category",
        json.dumps(jsonable_encoder(result)),
        ex=settings.redis.cache_expire_seconds)

    return result


@equipments_router.get("/{category_slug}/{path:path}",
                       response_model=Optional[Union[EquipmentResponse, EquipmentSchema]])
async def get_equipment_or_equipments(
        session: Annotated[AsyncSession, Depends(get_async_session)],
        redis_client: Annotated[Redis, Depends(get_redis)],
        category_slug,
        path: str,
        limit: int | None = 10,
        page: int | None = 1,
):
    equipment_service = EquipmentService(session)
    category_service = CategoryService(session)

    path = path.split("/")
    if len(path) == 2:
        key = f"{path[1]+"/"+ category_slug + "/" + path[0]}"
        if cached := await redis_client.get(key):
            return json.loads(cached)
        result= await equipment_service.get_single_equipment(path[1], category_slug + "/" + path[0])
        await redis_client.set(
            key,
            json.dumps(jsonable_encoder(result)),
            ex=settings.redis.cache_expire_seconds)
        return result
    if len(path) == 1:
        if await category_service.is_category(category_slug + "/" + path[0]):
            key = category_slug + "/" + path[0]
            if cached := await redis_client.get(key):
                return json.loads(cached)
            equipments = await equipment_service.get_equipments_by_category(limit, page, category_slug + "/" + path[0])
            await redis_client.set(
                key,
                json.dumps(jsonable_encoder(equipments)),
                ex=settings.redis.cache_expire_seconds)
            return equipments
        else:
            key = path[0]+"/"+ category_slug
            if cached := await redis_client.get(key):
                return json.loads(cached)
            result= await equipment_service.get_single_equipment(path[0], category_slug)
            await redis_client.set(
                key,
                json.dumps(jsonable_encoder(result)),
                ex=settings.redis.cache_expire_seconds)
            return result

@equipments_router.get("/{category_slug}", response_model=Union[EquipmentResponse, CategoryResponse])
async def get_equipments_or_categories(
        session: Annotated[AsyncSession, Depends(get_async_session)],
        redis_client: Annotated[Redis, Depends(get_redis)],
        category_slug: str,
        limit: int | None = 10,
        page: int | None = 1,

):
    print("Wd")
    if cached := await redis_client.get(f"category_slug/{category_slug}"):
        return json.loads(cached)
    category_service = CategoryService(session)
    equipment_service = EquipmentService(session)
    result = await category_service.get_child_categories(category_slug)
    if result is None:
        return await equipment_service.get_equipments_by_category(limit, page, category_slug)
    await redis_client.set(
        f"category_slug/{category_slug}",
        json.dumps(jsonable_encoder(result)),
        ex=settings.redis.cache_expire_seconds)

    return result


@equipments_router.get("", response_model=CategoryResponse)
async def get_categories(
        session: Annotated[AsyncSession, Depends(get_async_session)],
        redis_client: Annotated[Redis, Depends(get_redis)]

):
    if cached := await redis_client.get("store"):
        return json.loads(cached)
    category_service = CategoryService(session)

    result = await category_service.get_categories()
    await redis_client.set(
        "store",
        json.dumps(jsonable_encoder(result)),
        ex=settings.redis.cache_expire_seconds)

    return result

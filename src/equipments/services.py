from typing import List, Optional, Any, Coroutine

from fastapi import HTTPException
from starlette import status

from database.models import Equipment
from equipments.schemas import EquipmentTitleSchema, EventEquipmentCategorySchema
from src.equipments.repositories import EquipmentRepository, CategoryRepository
from src.equipments.schemas import EquipmentSchema, EquipmentResponse, CategoryResponse, EquipmentCategorySchema, \
    CategorySchema, EventEquipmentCategoryResponse


class EquipmentService:

    def __init__(self, session):
        self.equipment_repository = EquipmentRepository(session)
        self.category_repository = CategoryRepository(session)

    async def get_equipments_by_category(
            self, limit: int, page: int, category: str
    ) -> EquipmentResponse:
        if page < 1:
            page = 1
        offset = (page - 1) * limit
        equipments = await self.equipment_repository.get_equipments_by_category(
            limit, offset, category
        )
        category = await self.category_repository.get_single_category(category_slug=category)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category does not exists"
            )
        equipments = [
            EquipmentCategorySchema(
                title=equipment.title,
                equipment_slug=equipment.equipment_slug,
                photo_url=equipment.photo_url,
                price=equipment.rental_price
            )
            for equipment in equipments
        ]

        return EquipmentResponse(
            equipments=equipments,
            description=category.description,
            title=category.title
        )

    async def get_single_equipment(
            self,
            equipment_slug: str,
            category_slug: str
    ) -> Optional[EquipmentSchema]:
        equipment = await self.equipment_repository.get_single_equipment_by_condition(
            Equipment.equipment_slug == equipment_slug,
            Equipment.category_slug == category_slug
        )
        if equipment is not None:
            return EquipmentSchema(
                title=equipment.title,
                description=equipment.description,
                characteristics=equipment.characteristics,
                photo_url=equipment.photo_url,
                price=equipment.rental_price
            )
        return None

    async def get_event_equipments(self):
        categories = await self.category_repository.get_categories()
        categories_result = []
        for category in categories:
            equipments = await self.equipment_repository.get_equipments_by_category(None, 0, category.category_slug)
            equipments = [
                EquipmentTitleSchema(title=equipment.title)
                for equipment in equipments
            ]
            category_schema = EventEquipmentCategorySchema(
                category_title=category.title,
                equipments_catalog=equipments
            )
            categories_result.append(category_schema)
        result = {"equipments": categories_result}

        return result


class CategoryService:
    def __init__(self, session):
        self.category_repository = CategoryRepository(session)

    async def get_categories(self,
                             ) -> CategoryResponse:
        categories = await self.category_repository.get_categories()

        categories = [
            CategorySchema(
                title=category.title,
                hint=category.hint,
                category_slug=category.category_slug,
                photo_url=category.photo_url,
                description=category.description
            )
            for category in categories
        ]

        return CategoryResponse(categories=categories)

    async def is_category(self, category):
        category = await self.category_repository.is_category(category)
        if category is None:
            return False
        return True

    async def get_child_categories(self,
                                   parent_category,
                                   ) -> Optional[CategoryResponse]:
        categories = await self.category_repository.get_child_categories(parent_category)

        if categories is None or len(categories) == 0:
            return None

        categories = [
            CategorySchema(
                title=category.title,
                hint=category.hint,
                category_slug=category.category_slug,
                photo_url=category.photo_url,
                description=category.description
            )
            for category in categories
        ]

        return CategoryResponse(categories=categories)

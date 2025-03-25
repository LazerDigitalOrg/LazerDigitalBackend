from typing import List

from src.equipments.repositories import EquipmentRepository, CategoryRepository
from src.equipments.schemas import EquipmentSchema, EquipmentResponse, CategoryResponse, EquipmentCategorySchema, \
    CategorySchema


class EquipmentService:

    def __init__(self, session):
        self.equipment_repository = EquipmentRepository(session)

    async def get_equipments_by_category(
            self, limit: int, page: int, category: str
    ) -> EquipmentResponse:
        if page < 1:
            page = 1
        offset = (page - 1) * limit
        equipments = await self.equipment_repository.get_equipments_by_category(
            limit, offset, category
        )

        equipments = [
            EquipmentCategorySchema(
                title=equipment.title,
                equipment_slug=equipment.equipment_slug,
                photo_url=equipment.photo_url
            )
            for equipment in equipments
        ]

        return EquipmentResponse(equipments=equipments)

    async def get_single_equipment(
            self,
            equipment_slug: str
    ) -> EquipmentSchema:
        equipment = await self.equipment_repository.get_single_equipment(equipment_slug)
        print(equipment.title)
        return EquipmentSchema(
            title=equipment.title,
            description=equipment.description,
            characteristics=equipment.characteristics,
            photo_url=equipment.photo_url,
        )


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

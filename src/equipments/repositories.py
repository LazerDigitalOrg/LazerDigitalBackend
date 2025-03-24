from sqlalchemy import select, desc, asc

from database.models import Equipment, Category

class EquipmentRepository:
    def __init__(self, session):
        self.session = session


    async def get_equipments_by_category(self, limit, offset, category):
        stmt = select(Equipment).where(Equipment.category_slug == category).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_single_equipment(self, equipment_slug):
        stmt = select(Equipment).where(Equipment.equipment_slug == equipment_slug)
        result = await self.session.execute(stmt)
        return result.scalars().one()

class CategoryRepository:
    def __init__(self, session):
        self.session = session


    async def get_categories(self):
        stmt = select(Category)
        result = await self.session.execute(stmt)
        return result.scalars().all()

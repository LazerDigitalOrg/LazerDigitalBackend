from sqlalchemy import select, desc, asc, and_

from database.models import Equipment, Category


class EquipmentRepository:
    def __init__(self, session):
        self.session = session

    async def get_equipments_by_category(self, limit, offset, category):
        stmt = select(Equipment).where(Equipment.category_slug == category).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_single_equipment(self, equipment_slug, category_slug):
        print(category_slug)
        stmt = select(Equipment).where(
            and_(Equipment.equipment_slug == equipment_slug, Equipment.category_slug == category_slug))
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()


class CategoryRepository:
    def __init__(self, session):
        self.session = session

    async def get_categories(self):
        stmt = select(Category)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_single_category(self,category_slug):
        stmt = select(Category).filter_by(category_slug=category_slug)
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def is_category(self, category_slug):
        stmt = select(Category).filter_by(category_slug=category_slug)
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def get_child_categories(self, category_slug):
        stmt = select(Category).where(Category.parent_category_slug == category_slug)
        result = await self.session.execute(stmt)
        return result.scalars().all()

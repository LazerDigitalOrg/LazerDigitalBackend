from sqlalchemy import select

from database.models import RoleEnum
from src.database.models import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    async def get_user(self, email: str):
        stmt = select(User).filter_by(email=email)
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def get_user_by_role(self, role: RoleEnum):
        stmt = select(User).where(User.role==role)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def add_user(self, username, password, phone_number, email):
        user = User(
            username=username,
            hashed_password=password,
            phone_number=phone_number,
            email=email,
            role=RoleEnum.USER
        )
        self.session.add(user)

        await self.session.commit()
        await self.session.refresh(user)
        return user

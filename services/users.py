from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.user import UserCreate
from settings.db import get_db
from utils.security import get_password_hash


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create(self, data: UserCreate) -> User:
        # Хешуємо пароль перед збереженням!
        hashed_pwd = get_password_hash(data.password)
        new_user = User(
            name=data.name,
            email=data.email,
            hashed_password=hashed_pwd,
            role="user",  # За замовчуванням всі реєструються як звичайні користувачі
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)

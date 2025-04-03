from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from schemas.user import UserInDB, UserCreate
from sqlalchemy import select, insert, update
from models.user import User
from core.security import get_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func

class UserRepository:
    """
    Репозиторий для CRUD-операций с пользователями 
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[UserInDB]:
        """
        Получение пользователя по ID
        """
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        user = result.scalars().first()
        return UserInDB.model_validate(user) if user else None

    async def get_by_email(self, user_email: str) -> Optional[UserInDB]:
        """
        Получение пользователя по почте
        """
        query = select(User).where(User.email == user_email)
        result = await self.session.execute(query)
        user = result.scalars().first()
        return UserInDB.model_validate(user) if user else None

    async def get_by_name(self, user_name: str) -> Optional[UserInDB]:
        """
        Получение пользователя по имени
        """
        query = select(User).where(User.name == user_name)
        result = await self.session.execute(query)
        user = result.scalars().first()
        return UserInDB.model_validate(user) if user else None

    async def create(self, user_data: UserCreate) -> Optional[UserInDB]:
        """
        Создание нового пользователя 
        """
        hashed_password = get_password_hash(user_data.password)
        user_dict = user_data.model_dump(exclude={"password"}) #преобразование модели в словарь с исключением поля password
        user_dict.update({"password_hash": hashed_password})
        try:
            stmt = insert(User).values(**user_dict).returning(User)
            result = await self.session.execute(stmt)
            await self.session.commit()
            created_user = result.scalars().first()
            return UserInDB.model_validate(created_user) if created_user else None
        except IntegrityError as e:
            await self.session.rollback()
            return None

    async def update_last_login(self, user_id: int) -> None:
        """
        Обновление времени последнего входа
        """
        stmt = update(User).where(User.id == user_id).values(last_login=func.now())
        await self.session.execute(stmt)
        await self.session.commit()
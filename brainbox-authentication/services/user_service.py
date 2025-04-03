from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user import UserRepository
from schemas.user import UserCreate, UserResponse, UserInDB
from typing import Optional
from core.security import verify_password

class UserService:
    """
    Сервис для работы с пользователями (бизнес-логика)
    """
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def register_user(self, user_data: UserCreate) -> Optional[UserResponse]:
        """
        Регистрация нового пользователя
        """
        if await self.repo.get_by_email(user_data.email):
            return None
        if await self.repo.get_by_name(user_data.name):
            return None
        user = await self.repo.create(user_data)
        if not user:
            return None
        return user

    async def auth_user(self, user_email: str, user_password: str) -> Optional[UserInDB]:
        """
        Авторизация пользователя
        """
        user = await self.repo.get_by_email(user_email)
        if not user:
            return None
        if not verify_password(user_password, user.password_hash):
            return None
        await self.repo.update_last_login(user.id)
        return user

    async def get_user_profile(self, user_id: int) -> Optional[UserResponse]:
        """
        Получение профиля пользователя (без важных данных)
        """
        user = await self.repo.get_by_id(user_id)
        if not user:
            return None
        return user
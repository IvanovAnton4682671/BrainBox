from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user import UserRepository
from schemas.user import UserCreate, UserResponse, UserInDB, UserAuth
from typing import Optional
from core.errors import BusinessError
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
            raise BusinessError({
                "code": "email_exists",
                "message": "Пользователь с такой почтой уже существует!"
            })
        if await self.repo.get_by_name(user_data.name):
            raise BusinessError({
                "code": "name_exists",
                "message": "Пользователь с таким именем уже существует!"
            })
        user = await self.repo.create(user_data)
        if not user:
            raise BusinessError({
                "code": "user_has_not_been_created",
                "message": "Пользователь не создан!"
            })
        return user

    async def auth_user(self, user_data: UserAuth) -> Optional[UserInDB]:
        """
        Авторизация пользователя
        """
        user = await self.repo.get_by_email(user_data.email)
        if not user:
            raise BusinessError({
                "code": "email_does_not_exist",
                "message": "Пользователь с такой почтой не существует!"
            })
        if not verify_password(user_data.password, user.password_hash):
            raise BusinessError({
                "code": "wrong_password",
                "message": "Неверный пароль!"
            })
        await self.repo.update_last_login(user.id)
        return user

    async def get_user_profile(self, user_id: int) -> Optional[UserResponse]:
        """
        Получение профиля пользователя (без важных данных)
        """
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise BusinessError({
                "code": "user_not_found",
                "message": "Пользователь не найден!"
            })
        return user
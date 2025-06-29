from core.logger import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user import UserRepository
from schemas.user import UserCreate, UserResponse, UserInDB, UserAuth
from typing import Optional
from core.errors import BusinessError
from core.security import verify_password

logger = setup_logger("services.user")

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
        try:
            logger.info(f"Попытка регистрации для пользователя email = {user_data.email}; name = {user_data.name}")
            if await self.repo.get_by_email(user_data.email):
                logger.warning(f"Пользователь с такой почтой уже существует: {user_data.email}")
                raise BusinessError({
                    "code": "email_exists",
                    "message": "Пользователь с такой почтой уже существует!"
                })
            if await self.repo.get_by_name(user_data.name):
                logger.warning(f"Пользователь с таким именем уже существует: {user_data.name}")
                raise BusinessError({
                    "code": "name_exists",
                    "message": "Пользователь с таким именем уже существует!"
                })
            user = await self.repo.create(user_data)
            if not user:
                logger.error(f"Пользователь не создан")
                raise BusinessError({
                    "code": "user_has_not_been_created",
                    "message": "Пользователь не создан!"
                })
            logger.info(f"Пользователь создан: user = {user}")
            sessionid = await self.repo.create_session(user.id)
            if not sessionid:
                logger.error(f"Сессия не создана")
                raise BusinessError({
                    "code": "sessionid_has_not_been_created",
                    "message": "Сессия не создана!"
                })
            logger.info(f"Сессия создана: sessionid = {sessionid}")
            logger.info(f"Вернули в ответе user = {user}, sessionid = {sessionid}")
            return {
                "user": user,
                "sessionid": sessionid
            }
        except Exception as e:
            logger.error(f"Ошибка при регистрации: {str(e)}", exc_info=True)
            raise

    async def auth_user(self, user_data: UserAuth) -> Optional[UserInDB]:
        """
        Авторизация пользователя
        """
        try:
            logger.info(f"Попытка авторизации для пользователя email = {user_data.email}")
            user = await self.repo.get_by_email(user_data.email)
            if not user:
                logger.warning(f"Пользователь с такой почтой не существует: {user_data.email}")
                raise BusinessError({
                    "code": "email_does_not_exist",
                    "message": "Пользователь с такой почтой не существует!"
                })
            if not verify_password(user_data.password, user.password_hash):
                logger.warning(f"Неверный пароль для пользователя: email = {user_data.email}")
                raise BusinessError({
                    "code": "wrong_password",
                    "message": "Неверный пароль!"
                })
            await self.repo.update_last_login(user.id)
            logger.info(f"Пользователь найден: id = {user.id}")
            sessionid = await self.repo.create_session(user.id)
            if not sessionid:
                logger.error(f"Сессия не создана")
                raise BusinessError({
                    "code": "sessionid_has_not_been_created",
                    "message": "Сессия не создана!"
                })
            logger.info(f"Сессия создана: sessionid = {sessionid}")
            logger.info(f"Вернули в ответе user = {user}, sessionid = {sessionid}")
            return {
                "user": user,
                "sessionid": sessionid
            }
        except Exception as e:
            logger.error(f"Ошибка при авторизации: {str(e)}", exc_info=True)
            raise

    async def get_user_profile(self, user_id: int) -> Optional[UserResponse]:
        """
        Получение профиля пользователя (без важных данных)
        """
        try:
            logger.info(f"Попытка получения профиля пользователя: id = {user_id}")
            user = await self.repo.get_by_id(user_id)
            if not user:
                logger.error(f"Пользователь не найден: id = {user_id}")
                raise BusinessError({
                    "code": "user_not_found",
                    "message": "Пользователь не найден!"
                })
            logger.info(f"Пользователь найден: id = {user.id}")
            logger.info("Вернули в ответе этого пользователя")
            return user
        except Exception as e:
            logger.error(f"Ошибка при получении профиля: {str(e)}", exc_info=True)
            raise

    async def logout_user(self, sessionid: str) -> None:
        """
        Удаление сессии пользователя
        """
        try:
            logger.info(f"Попытка удалить сессию: sessionid = {sessionid}")
            await self.repo.delete_session(sessionid)
            logger.info(f"Сессия удалена")
        except Exception as e:
            logger.error(f"Ошибка при удалении сессии: {str(e)}", exc_info=True)
            raise
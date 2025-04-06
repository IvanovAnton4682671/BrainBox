from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from schemas.user import UserInDB, UserCreate
from sqlalchemy import select, insert, update
from models.user import User
from core.security import get_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from core.logger import setup_logger

logger = setup_logger("repositories/user.py")

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
        try:
            logger.info(f"Попытка получить пользователя по id: {user_id}")
            query = select(User).where(User.id == user_id)
            result = await self.session.execute(query)
            user = result.scalars().first()
            logger.info(f"Пользователь получен: id - {user.id}")
            return UserInDB.model_validate(user) if user else None
        except Exception as e:
            logger.error(f"Ошибка при получении пользователя по id: {str(e)}", exc_info=True)
            raise

    async def get_by_email(self, user_email: str) -> Optional[UserInDB]:
        """
        Получение пользователя по почте
        """
        try:
            logger.info(f"Попытка получить пользователя по email: {user_email}")
            query = select(User).where(User.email == user_email)
            result = await self.session.execute(query)
            user = result.scalars().first()
            logger.info(f"Пользователь получен: id - {user.id}")
            return UserInDB.model_validate(user) if user else None
        except Exception as e:
            logger.error(f"Ошибка при получении пользователя по email: {str(e)}", exc_info=True)
            raise

    async def get_by_name(self, user_name: str) -> Optional[UserInDB]:
        """
        Получение пользователя по имени
        """
        try:
            logger.info(f"Попытка получить пользователя по name: {user_name}")
            query = select(User).where(User.name == user_name)
            result = await self.session.execute(query)
            user = result.scalars().first()
            logger.info(f"Пользователь получен: id - {user.id}")
            return UserInDB.model_validate(user) if user else None
        except Exception as e:
            logger.error(f"Ошибка при получении пользователя по name: {str(e)}", exc_info=True)
            raise

    async def create(self, user_data: UserCreate) -> Optional[UserInDB]:
        """
        Создание нового пользователя 
        """
        try:
            logger.info(f"Попытка создать пользователя: email - {user_data.email}, name - {user_data.name}")
            hashed_password = get_password_hash(user_data.password)
            user_dict = user_data.model_dump(exclude={"password"}) #преобразование модели в словарь с исключением поля password
            user_dict.update({"password_hash": hashed_password})
            try:
                stmt = insert(User).values(**user_dict).returning(User)
                result = await self.session.execute(stmt)
                await self.session.commit()
                created_user = result.scalars().first()
                logger.info(f"Пользователь создан: id - {created_user.id}")
                return UserInDB.model_validate(created_user) if created_user else None
            except IntegrityError as e:
                await self.session.rollback()
                logger.warning(f"Нарушение целостности БД при попытке создать пользователя: email - {user_data.email}, name - {user_data.name}")
                raise IntegrityError({
                    "code": "register_integrity_error",
                    "message": "Нарушение целостности БД при попытке создать пользователя!"
                })
        except Exception as e:
            logger.error(f"Ошибка при создании пользователя: {str(e)}", exc_info=True)
            raise

    async def update_last_login(self, user_id: int) -> None:
        """
        Обновление времени последнего входа
        """
        try:
            logger.info(f"Попытка обновить время входа в аккаунт: id - {user_id}")
            stmt = update(User).where(User.id == user_id).values(last_login=func.now())
            await self.session.execute(stmt)
            await self.session.commit()
            logger.info(f"Время входа обновлено: id - {user_id}")
        except Exception as e:
            logger.error(f"Ошибка при обновлении времени входа в аккаунт: id - {user_id}")
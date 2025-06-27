from core.logger import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.text import TextMessageCreate, TextMessageResponse, UserID, MessageText, TextMessageInDB
from typing import Optional, List
from models.text import TextMessage
from sqlalchemy import select, desc

logger = setup_logger("repositories.text")

class TextRepository:
    """
    Репозиторий для CRUD-операций для текстовых сообщений
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_message(self, message: TextMessageCreate) -> Optional[TextMessageResponse]:
        try:
            logger.info(f"Пробуем создать сообщение с данными: message = {message}")
            query = TextMessage(
                user_id=message.user_id,
                is_from_user=message.is_from_user,
                message_text=message.message_text
            )
            self.session.add(query)
            await self.session.commit()
            await self.session.refresh(query)
            logger.info("Создали сообщение, возвращаем из бд")
            return TextMessageResponse.model_validate(query.to_dict()) if query else None
        except Exception as e:
            logger.error(f"Ошибка при создании сообщения: {str(e)}", exc_info=True)
            await self.session.rollback()
            raise

    async def get_messages_by_user_id(self, user_id: UserID) -> Optional[List[TextMessageResponse]]:
        try:
            logger.info(f"Пробуем получить сообщения пользователя user_id = {user_id}")
            query = select(TextMessage).where(TextMessage.user_id == user_id).order_by(desc(TextMessage.created_at))
            result = await self.session.execute(query)
            messages = result.scalars().all()
            logger.info(f"Сообщения пользователя user_id = {user_id} получили")
            return [TextMessageResponse.model_validate(msg.to_dict()) for msg in messages] if messages else None
        except Exception as e:
            logger.error(f"Ошибка получения сообщений: {str(e)}", exc_info=True)
            raise

    async def get_message_by_message_text(self, message_text: MessageText) -> Optional[TextMessageInDB]:
        try:
            logger.info(f"Пробуем получить сообщение по message_text = {message_text}")
            query = select(TextMessage).where(TextMessage.message_text == message_text)
            result = await self.session.execute(query)
            message = result.scalars().first()
            logger.info(f"Сообщение с message_text = {message_text} получили")
            return TextMessageInDB.model_validate(message.to_dict()) if message else None
        except Exception as e:
            logger.error(f"Ошибка получения сообщения: {str(e)}", exc_info=True)
            raise

    async def delete_messages(self, user_id: UserID) -> None:
        try:
            logger.info(f"Пробуем удалить сообщения пользователя user_id = {user_id}")
            messages = await self.get_messages_by_user_id(user_id)
            if not messages:
                logger.info(f"У пользователя user_id = {user_id} сообщений нет")
                return
            query = TextMessage.__table__.delete().where(TextMessage.user_id == user_id)
            await self.session.execute(query)
            await self.session.commit()
            logger.info(f"Сообщение пользователя user_id = {user_id} удалены")
            return
        except Exception as e:
            logger.error(f"Ошибка удаления сообщений: {str(e)}", exc_info=True)
            await self.session.rollback()
            raise
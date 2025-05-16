from core.logger import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.text import TextMessageCreate, TextMessageResponse, UserID, MessageText, TextMessageInDB
from typing import Optional, List
from models.text import TextMessage
from sqlalchemy import select, desc

logger = setup_logger("repositories/text.py")

class TextRepository:
    """
    Репозиторий для CRUD-операций для текстовых сообщений
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_message(self, message: TextMessageCreate) -> Optional[TextMessageResponse]:
        try:
            query = TextMessage(
                user_id=message.user_id,
                is_from_user=message.is_from_user,
                message_text=message.message_text
            )
            self.session.add(query)
            await self.session.commit()
            await self.session.refresh(query)
            return TextMessageResponse.model_validate(query.to_dict()) if query else None
        except Exception as e:
            logger.error(f"Ошибка создания текстового сообщения: {str(e)}", exc_info=True)
            await self.session.rollback()
            raise

    async def get_messages_by_user_id(self, user_id: UserID) -> Optional[List[TextMessageResponse]]:
        try:
            query = select(TextMessage).where(TextMessage.user_id == user_id).order_by(desc(TextMessage.created_at))
            result = await self.session.execute(query)
            messages = result.scalars().all()
            return [TextMessageResponse.model_validate(msg.to_dict()) for msg in messages] if messages else None
        except Exception as e:
            logger.error(f"Ошибка получения текстовых сообщений: {str(e)}", exc_info=True)
            raise

    async def get_message_by_message_text(self, message_text: MessageText) -> Optional[TextMessageInDB]:
        try:
            query = select(TextMessage).where(TextMessage.message_text == message_text)
            result = await self.session.execute(query)
            message = result.scalars().first()
            return TextMessageInDB.model_validate(message.to_dict()) if message else None
        except Exception as e:
            logger.error(f"Ошибка получения сообщения по тексту: {str(e)}", exc_info=True)
            raise

    async def delete_messages(self, user_id: UserID) -> None:
        try:
            messages = await self.get_messages_by_user_id(user_id)
            if not messages:
                return
            query = TextMessage.__table__.delete().where(TextMessage.user_id == user_id)
            await self.session.execute(query)
            await self.session.commit()
            return
        except Exception as e:
            logger.error(f"Ошибка удаления текстовых сообщений: {str(e)}", exc_info=True)
            await self.session.rollback()
            raise
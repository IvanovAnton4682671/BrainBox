from core.logger import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.audio import AudioMessageCreate, AudioMessageResponse
from typing import Optional, List
from sqlalchemy import select, desc
from models.audio import AudioMessage
from uuid import UUID

logger = setup_logger("repositories.audio")

class AudioRepository:
    """
    Репозиторий для CRUD-операций для аудио-сообщений
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_message(self, message: AudioMessageCreate) -> Optional[AudioMessageResponse]:
        try:
            logger.info(f"Пробуем создать сообщение с данными: message = {message}")
            query = AudioMessage(
                user_id=message.user_id,
                is_from_user=message.is_from_user,
                message_text=message.message_text,
                audio_uid=str(message.audio_uid) if message.audio_uid else None
            )
            self.session.add(query)
            await self.session.commit()
            await self.session.refresh(query)
            logger.info("Сообщение создано, возвращаем из бд")
            return AudioMessageResponse.model_validate(query) if query else None
        except Exception as e:
            logger.error(f"Ошибка при создании сообщения: {str(e)}", exc_info=True)
            await self.session.rollback()
            raise

    async def get_user_messages(self, user_id: int) -> Optional[List[AudioMessageResponse]]:
        logger.info(f"Пробуем получить сообщения пользователя по user_id = {user_id}")
        query = select(AudioMessage).where(AudioMessage.user_id == user_id).order_by(desc(AudioMessage.created_at))
        result = await self.session.execute(query)
        messages = result.scalars().all()
        logger.info(f"Получили сообщения пользователя user_id = {user_id}")
        return [AudioMessageResponse.model_validate(msg) for msg in messages] if messages else None

    async def get_message_by_uid(self, audio_uid: UUID) -> Optional[AudioMessageResponse]:
        logger.info(f"Пробуем получить сообщение по audio_uid = {audio_uid}")
        query = select(AudioMessage).where(AudioMessage.audio_uid == str(audio_uid))
        result = await self.session.execute(query)
        message = result.scalars().first()
        logger.info(f"Получили сообщение c audio_uid = {audio_uid}")
        return AudioMessageResponse.model_validate(message) if message else None

    async def delete_user_messages(self, user_id: int) -> None:
        try:
            logger.info(f"Пробуем удалить все сообщения пользователя user_id = {user_id}")
            messages = self.get_user_messages(user_id)
            if not messages:
                logger.info(f"У пользователя user_id = {user_id} нет сообщений")
                return
            query = AudioMessage.__table__.delete().where(AudioMessage.user_id == user_id)
            await self.session.execute(query)
            await self.session.commit()
            logger.info(f"Удалили сообщения пользователя user_id = {user_id}")
            return
        except Exception as e:
            logger.error(f"Ошибка при удалении сообщений: {str(e)}", exc_info=True)
            await self.session.rollback()
            raise
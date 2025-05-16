from core.logger import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.text import TextRepository
from yandex_cloud_ml_sdk import YCloudML
from core.config import settings
from schemas.text import MessageText, UserID, IsFromUser, TextMessageResponse
from models.text import TextMessage
from typing import Optional, List

logger = setup_logger("services/text.py")

class TextService:
    def __init__(self, session: AsyncSession):
        self.repo = TextRepository(session)
        sdk = YCloudML(
            folder_id=settings.FOLDER_ID,
            auth=settings.OAUTH_TOKEN
        )
        self.model = sdk.models.completions("yandexgpt")
        self.model = self.model.configure(temperature=0.3)

    def _generate_answer(self, message_text: MessageText) -> MessageText:
        """
        Генерирует ответ через обращение к YandexGPT API
        """
        try:
            result = self.model.run(message_text)
            return result.alternatives[0].text
        except Exception as e:
            logger.error(f"Ошибка генерации ответа через YandexGPT API: {str(e)}", exc_info=True)
            raise

    async def _save_message(self, user_id: UserID, is_from_user: IsFromUser, message_text: MessageText) -> None:
        """
        Сохраняет сообщение в БД
        """
        try:
            system_message = TextMessage(
                user_id=user_id,
                is_from_user=is_from_user,
                message_text=message_text
            )
            await self.repo.create_message(system_message)
        except Exception as e:
            logger.error(f"Ошибка сохранения сообщения: {str(e)}", exc_info=True)
            raise

    async def create_answer(self, user_id: UserID, text: MessageText) -> Optional[TextMessageResponse]:
        """
        Получает сообщение пользователя и создаёт для него ответ
        """
        try:
            await self._save_message(user_id, True, text)
            answer = self._generate_answer(text)
            await self._save_message(user_id, False, answer)
            saved_system_message = await self.repo.get_message_by_message_text(answer)
            return TextMessageResponse(
                is_from_user=saved_system_message.is_from_user,
                message_text=saved_system_message.message_text,
                created_at=saved_system_message.created_at
            )
        except Exception as e:
            logger.error(f"Ошибка создания ответа: {str(e)}", exc_info=True)
            raise

    async def get_messages(self, user_id: UserID) -> Optional[List[TextMessageResponse]]:
        """
        Загружает всю историю чата
        """
        try:
            messages = await self.repo.get_messages_by_user_id(user_id)
            return messages
        except Exception as e:
            logger.error(f"Ошибка загрузки истории чата: {str(e)}", exc_info=True)
            raise

    async def delete_messages(self, user_id: UserID) -> None:
        """
        Удаляет всю историю чата
        """
        try:
            messages = await self.repo.get_messages_by_user_id(user_id)
            if not messages:
                return
            await self.repo.delete_messages(user_id)
            return
        except Exception as e:
            logger.error(f"Ошибка удаления истории чата: {str(e)}", exc_info=True)
            raise
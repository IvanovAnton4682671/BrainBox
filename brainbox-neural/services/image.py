from core.logger import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from yandex_cloud_ml_sdk import YCloudML
from core.config import settings
from repositories.image import ImageRepository
from schemas.image import MessageText, UserID, ImageMessageInDB, ImageMessageResponse, ImageMessageRequest
from core.storage import image_storage
from uuid import uuid4
import pathlib
from typing import List
from models.image import ImageMessage

logger = setup_logger("services/image.py")

class ImageService:
    def __init__(self, session: AsyncSession):
        self.repo = ImageRepository(session)
        sdk = YCloudML(
            folder_id=settings.FOLDER_ID,
            auth=settings.OAUTH_TOKEN
        )
        self.model = sdk.models.image_generation("yandex-art")
        self.model = self.model.configure(width_ratio=2, height_ratio=1, seed=1863)

    async def _save_user_message(self, message: ImageMessageRequest) -> ImageMessageInDB:
        try:
            saved_message = await self.repo.create_user_message(message)
            return saved_message
        except Exception as e:
            logger.error(f"Ошибка сохранения сообщения пользователя: {str(e)}", exc_info=True)
            raise

    async def _generate_image(self, text: MessageText) -> bytes:
        operation = self.model.run_deferred(text)
        result = operation.wait()
        return result.image_bytes

    async def _save_image_minio(self, image_data: bytes) -> str:
        try:
            saved_image_uid = await image_storage.upload_image(image_data)
            return saved_image_uid
        except Exception as e:
            logger.error(f"Ошибка сохранения картинки в MinIO: {str(e)}", exc_info=True)
            raise

    async def _save_image_db(self, user_id: UserID, image_uid: str) -> ImageMessageInDB:
        try:
            message = ImageMessage(
                user_id=user_id,
                is_from_user=False,
                image_uid=image_uid
            )
            saved_message = await self.repo.create_system_message(message)
            return saved_message
        except Exception as e:
            logger.error(f"Ошибка сохранения картинки в БД: {str(e)}", exc_info=True)
            raise

    async def create_answer(self, message: ImageMessageRequest) -> ImageMessageResponse:
        try:
            user_message = await self._save_user_message(message)
            image = await self._generate_image(user_message.message_text)
            image_uid = await self._save_image_minio(image)
            system_message = await self._save_image_db(user_message.user_id, image_uid)
            return system_message
        except Exception as e:
            logger.error(f"Ошибка создания системного ответа: {str(e)}", exc_info=True)
            raise

    async def get_user_messages(self, user_id: UserID) -> List[ImageMessageInDB]:
        try:
            messages = await self.repo.get_user_messages(user_id)
            return messages
        except Exception as e:
            logger.error(f"Ошибка при получении всех сообщений: {str(e)}", exc_info=True)
            raise

    async def delete_user_messages(self, user_id: UserID) -> None:
        try:
            messages = await self.repo.get_user_messages(user_id)
            if not messages:
                return
            for msg in messages:
                if msg.image_uid:
                    image_storage.client.remove_object(
                        bucket_name=image_storage.bucket,
                        object_name=str(msg.image_uid)
                    )
            await self.repo.delete_user_messages(user_id)
            return
        except Exception as e:
            logger.error(f"Ошибка при удалении всех сообщений чата: {str(e)}", exc_info=True)
            raise
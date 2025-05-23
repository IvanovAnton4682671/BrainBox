from core.logger import setup_logger
from core.config import settings
from httpx import AsyncClient, Timeout, Limits, AsyncHTTPTransport

logger = setup_logger("interfaces/image.py")

class ImageInterface:
    def __init__(self):
        self.base_url = f"{settings.NEURAL_SERVICE_URL}/image"
        self.client = AsyncClient(
            timeout=Timeout(60.0),
            limits=Limits(max_connections=100),
            transport=AsyncHTTPTransport(retries=3)
        )

    async def generate_answer(self, headers: dict, text: str):
        try:
            logger.info("Получен /generate-answer запрос для сервиса нейросетей!")
            return await self.client.post(
                url=f"{self.base_url}/generate-answer",
                headers=headers,
                json={"text": text}
            )
        except Exception as e:
            logger.error(f"Ошибка генерации ответа: {str(e)}", exc_info=True)
            raise

    async def view_image(self, headers: dict, image_uid: str):
        try:
            logger.info("Получен /view/{image_uid} запрос для сервис нейросетей!")
            return await self.client.get(
                url=f"{self.base_url}/view/{image_uid}",
                headers=headers
            )
        except Exception as e:
            logger.error(f"Ошибка отображения картинки: {str(e)}", exc_info=True)
            raise

    async def download_image(self, headers: dict, image_uid: str):
        try:
            logger.info("Получен /download/{image_uid} запрос для сервиса нейросетей!")
            return await self.client.get(
                url=f"{self.base_url}/download/{image_uid}",
                headers=headers
            )
        except Exception as e:
            logger.error(f"Ошибка скачивания картинки: {str(e)}", exc_info=True)
            raise

    async def get_image_messages(self, headers: dict):
        try:
            logger.info("Получен /get-image-messages запрос для сервиса нейросетей!")
            return await self.client.get(
                url=f"{self.base_url}/get-image-messages",
                headers=headers
            )
        except Exception as e:
            logger.error(f"Ошибка получения истории чата: {str(e)}", exc_info=True)
            raise

    async def delete_image_messages(self, headers: dict):
        try:
            logger.info("Получен /delete-image-messages запрос для сервиса нейросетей!")
            return await self.client.delete(
                url=f"{self.base_url}/delete-image-messages",
                headers=headers
            )
        except Exception as e:
            logger.error(f"Ошибка удаления истории чата: {str(e)}", exc_info=True)
            raise

image_interface = ImageInterface()
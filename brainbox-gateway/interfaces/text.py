from core.logger import setup_logger
from core.config import settings
import httpx

logger = setup_logger("interfaces/text.py")

class TextInterface:
    def __init__(self):
        self.base_url = f"{settings.NEURAL_SERVICE_URL}/text"
        self.client = httpx.AsyncClient(timeout=60.0)

    async def generate_answer(self, headers: dict, text: str):
        logger.info("Получен /generate-answer запрос для сервиса нейросетей!")
        return await self.client.post(
            f"{self.base_url}/generate-answer",
            headers=headers,
            json={
                "text": text
            }
        )

    async def get_text_messages(self, headers: dict):
        logger.info("Получен /get-text-messages запрос для сервиса нейросетей!")
        return await self.client.get(
            f"{self.base_url}/get-text-messages",
            headers=headers
        )

    async def delete_text_messages(self, headers: dict):
        logger.info("Получен /delete-text-messages запрос для сервиса нейросетей!")
        return await self.client.delete(
            f"{self.base_url}/delete-text-messages",
            headers=headers
        )

text_interface = TextInterface()
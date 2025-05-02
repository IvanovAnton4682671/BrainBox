from core.logger import setup_logger
from core.config import settings
import httpx

logger = setup_logger("interfaces/neural.py")

class NeuralService:
    def __init__(self):
        self.base_url = f"{settings.NEURAL_SERVICE_URL}/neural"
        self.client = httpx.AsyncClient(timeout=60.0)

    async def recognize_audio(self, headers: dict, file: bytes, filename: str):
        logger.info("Получен /recognize-audio запрос для сервиса нейросетей!")
        files = {"file": (filename, file, "audio/*")}
        return await self.client.post(
            f"{self.base_url}/recognize-audio",
            headers=headers,
            files=files
        )

    async def get_audio_messages(self, headers: dict):
        logger.info("Получен /get-audio-messages запрос для сервиса нейросетей!")
        return await self.client.get(
            f"{self.base_url}/get-audio-messages",
            headers=headers
        )

neural_service = NeuralService()
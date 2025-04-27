from core.logger import setup_logger
from core.config import settings
import httpx

logger = setup_logger("interfaces/neural.py")

class NeuralService:
    def __init__(self):
        self.base_url = f"{settings.NEURAL_SERVICE_URL}/neural"
        self.client = httpx.AsyncClient(timeout=60.0)

    async def recognize_audio(self, file: bytes, filename: str):
        logger.info("Получен /recognize-audio запрос для сервиса нейросетей!")
        files = {"file": (filename, file, "audio/*")}
        return await self.client.post(
            f"{self.base_url}/recognize-audio",
            files=files
        )

neural_service = NeuralService()
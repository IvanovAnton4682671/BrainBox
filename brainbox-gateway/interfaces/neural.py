from core.logger import setup_logger
from core.config import settings
import httpx

logger = setup_logger("interfaces/neural.py")

class NeuralService:
    def __init__(self):
        self.base_url = f"{settings.NEURAL_SERVICE_URL}/neural"
        self.client = httpx.AsyncClient(timeout=60.0)

    async def upload_audio(self, headers: dict, file: bytes, filename: str):
        logger.info("Получен /upload-audio запрос для сервиса нейросетей!")
        files = {"file": (filename, file, "audio/*")}
        return await self.client.post(
            f"{self.base_url}/upload-audio",
            headers=headers,
            files=files
        )

    async def recognize_saved_audio(self, headers: dict, audio_uid: str):
        try:
            logger.info("Получен /recognize_saved_audio запрос для сервиса нейросетей!")
            return await self.client.post(
                f"{self.base_url}/recognize-saved-audio",
                headers=headers,
                json={ "audio_uid": audio_uid }
            )
        except Exception as e:
            raise

    async def get_audio_messages(self, headers: dict):
        logger.info("Получен /get-audio-messages запрос для сервиса нейросетей!")
        return await self.client.get(
            f"{self.base_url}/get-audio-messages",
            headers=headers
        )

    async def download_audio(self, headers: dict, audio_uid: str):
        logger.info("Получили /download-audio/{audio_uid} запрос для сервиса нейросетей!")
        return await self.client.get(
            f"{self.base_url}/download-audio/{audio_uid}",
            headers=headers
        )

    async def delete_audio_messages(self, headers: dict):
        logger.info("Получен /delete-audio-messages запрос для сервиса нейросетей!")
        return await self.client.delete(
            f"{self.base_url}/delete-audio-messages",
            headers=headers
        )

neural_service = NeuralService()
from core.logger import setup_logger
from core.config import settings
from httpx import AsyncClient, Timeout, Limits, AsyncHTTPTransport

logger = setup_logger("interfaces/audio.py")

class AudioInterface:
    def __init__(self):
        self.base_url = f"{settings.NEURAL_SERVICE_URL}/audio"
        self.client = AsyncClient(
            timeout=Timeout(10.0),
            limits=Limits(max_connections=100),
            transport=AsyncHTTPTransport(retries=3)
        )

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

audio_interface = AudioInterface()
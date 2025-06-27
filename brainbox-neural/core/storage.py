from core.logger import setup_logger
from minio import Minio
from core.config import settings
from uuid import uuid4
import io

logger = setup_logger("core.storage")

class AudioStorage:
    def __init__(self):
        self.client = Minio(
            endpoint=settings.MINIO_URL,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.bucket = settings.MINIO_BUCKET_AUDIO
        self._ensure_bucket()

    def _ensure_bucket(self):
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)
            logger.info(f"Не было бакета {self.bucket}, создали")

    async def upload_audio(self, file_data: bytes) -> str:
        audio_uid = str(uuid4())
        try:
            self.client.put_object(
                bucket_name=self.bucket,
                object_name=audio_uid,
                data=io.BytesIO(file_data),
                length=len(file_data),
                content_type="audio/mpeg"
            )
            logger.info(f"Сохранили аудио-файл с audio_uid = {audio_uid}, вернули audio_uid")
            return audio_uid
        except Exception as e:
            logger.error(f"Ошибка при сохранении аудио-файла: {str(e)}", exc_info=True)
            raise

    async def download_audio(self, audio_uid: str) -> bytes:
        try:
            response = self.client.get_object(
                bucket_name=self.bucket,
                object_name=audio_uid
            )
            logger.info(f"Скачали аудио-файл по audio_uid = {audio_uid}, вернули поток байтов")
            return response.read()
        except Exception as e:
            logger.error(f"Ошибка при скачивании аудио-файла: {str(e)}", exc_info=True)
            raise
        finally:
            response.close()
            response.release_conn()

class ImageStorage:
    def __init__(self):
        self.client = Minio(
            endpoint=settings.MINIO_URL,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.bucket = settings.MINIO_BUCKET_IMAGE
        self._ensure_bucket()

    def _ensure_bucket(self):
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)
            logger.info(f"Не было бакета {self.bucket}, создали")

    async def upload_image(self, file_data: bytes) -> str:
        image_uid = str(uuid4())
        try:
            self.client.put_object(
                bucket_name=self.bucket,
                object_name=image_uid,
                data=io.BytesIO(file_data),
                length=len(file_data),
                content_type="image/jpeg"
            )
            logger.info(f"Сохранили картинку с image_uid = {image_uid}, вернули image_uid")
            return image_uid
        except Exception as e:
            logger.error(f"Ошибка при сохранении картинки: {str(e)}", exc_info=True)
            raise

    async def download_image(self, image_uid: str) -> bytes:
        try:
            response = self.client.get_object(
                bucket_name=self.bucket,
                object_name=image_uid
            )
            logger.info(f"Скачали картинку по image_uid = {image_uid}, вернули поток байтов")
            return response.read()
        except Exception as e:
            logger.error(f"Ошибка при скачивании картинки: {str(e)}", exc_info=True)
            raise
        finally:
            response.close()
            response.release_conn()

audio_storage = AudioStorage()

image_storage = ImageStorage()
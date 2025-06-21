from minio import Minio
from core.config import settings
from uuid import uuid4
import io

class AudioStorage:
    def __init__(self):
        self.client = Minio(
            #endpoint=settings.MINIO_URL,
            endpoint="localhost:30001",
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.bucket = settings.MINIO_BUCKET_AUDIO
        self._ensure_bucket()

    def _ensure_bucket(self):
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

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
            return audio_uid
        except Exception as e:
            raise

    async def download_audio(self, audio_uid: str) -> bytes:
        try:
            response = self.client.get_object(
                bucket_name=self.bucket,
                object_name=audio_uid
            )
            return response.read()
        except Exception as e:
            raise
        finally:
            response.close()
            response.release_conn()

class ImageStorage:
    def __init__(self):
        self.client = Minio(
            #endpoint=settings.MINIO_URL,
            endpoint="localhost:30001",
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.bucket = settings.MINIO_BUCKET_IMAGE
        self._ensure_bucket()

    def _ensure_bucket(self):
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

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
            return image_uid
        except Exception as e:
            raise

    async def download_image(self, image_uid: str) -> bytes:
        try:
            response = self.client.get_object(
                bucket_name=self.bucket,
                object_name=image_uid
            )
            return response.read()
        except Exception as e:
            raise
        finally:
            response.close()
            response.release_conn()

audio_storage = AudioStorage()

image_storage = ImageStorage()
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    MINIO_URL: str = Field(..., min_length=1)
    MINIO_ACCESS_KEY: str = Field(..., min_length=1)
    MINIO_SECRET_KEY: str = Field(..., min_length=1)
    MINIO_SECURE: bool = False
    MINIO_BUCKET_AUDIO: str = Field(..., min_length=1)
    MINIO_BUCKET_IMAGE: str = Field(..., min_length=1)

    POSTGRES_URL: str = Field(..., min_length=1)

    RABBITMQ_URL: str = Field(..., min_length=1)
    RABBITMQ_AUDIO_REQUESTS: str = Field(..., min_length=1)
    RABBITMQ_AUDIO_RESPONSES: str = Field(..., min_length=1)
    RABBITMQ_IMAGE_REQUESTS: str = Field(..., min_length=1)
    RABBITMQ_IMAGE_RESPONSES: str = Field(..., min_length=1)
    RABBITMQ_TEXT_REQUESTS: str = Field(..., min_length=1)
    RABBITMQ_TEXT_RESPONSES: str = Field(..., min_length=1)

    REDIS_URL: str = Field(..., min_length=1)

    NEURAL_HOST: str = Field(..., min_length=1)
    NEURAL_PORT: int = Field(..., ge=1, le=65535)
    APP_DEBUG: bool = False

    FOLDER_ID: str = Field(..., min_length=1)
    OAUTH_TOKEN: str = Field(..., min_length=1)

    GATEWAY_URL: str = Field(..., min_length=1)

    AUTH_SERVICE_URL: str = Field(..., min_length=1)

    class Config:
        env_file = ".env"

settings = Settings()
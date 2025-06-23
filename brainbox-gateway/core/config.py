from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    RABBITMQ_URL: str = Field(..., min_length=1)
    RABBITMQ_AUDIO_REQUESTS: str = Field(..., min_length=1)
    RABBITMQ_AUDIO_RESPONSES: str = Field(..., min_length=1)
    RABBITMQ_IMAGE_REQUESTS: str = Field(..., min_length=1)
    RABBITMQ_IMAGE_RESPONSES: str = Field(..., min_length=1)
    RABBITMQ_TEXT_REQUESTS: str = Field(..., min_length=1)
    RABBITMQ_TEXT_RESPONSES: str = Field(..., min_length=1)

    REDIS_URL: str = Field(..., min_length=1)

    GATEWAY_HOST: str = Field(..., min_length=1)
    GATEWAY_PORT: int = Field(..., ge=1, le=65535)

    CLIENT_URL: str = Field(..., min_length=1)
    CLIENT_URL_NODE: str = Field(..., min_length=1)

    AUTH_SERVICE_URL: str = Field(..., min_length=1)

    NEURAL_SERVICE_URL: str = Field(..., min_length=1)

    class Config:
        env_file = ".env"

settings = Settings()
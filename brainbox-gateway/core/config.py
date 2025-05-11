from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    GATEWAY_HOST: str = Field(..., min_length=1)
    GATEWAY_PORT: int = Field(..., ge=1, le=65535)

    CLIENT_URL: str = Field(..., min_length=1)

    AUTH_SERVICE_URL: str = Field(..., min_length=1)

    RABBITMQ_URL: str = Field(..., min_length=1)
    RABBITMQ_AUDIO_REQUESTS: str = Field(..., min_length=1)
    RABBITMQ_AUDIO_RESPONSES: str = Field(..., min_length=1)

    REDIS_HOST: str = Field(..., min_length=1)
    REDIS_PORT: int = Field(..., ge=1, le=65535)
    REDIS_DB: int = Field(..., ge=0, le=65535)
    REDIS_URL: Optional[str] = None

    NEURAL_SERVICE_URL: str = Field(..., min_length=1)

    @classmethod
    def assemble_redis_connection(cls, values: dict) -> str:
        return f"redis://{values['REDIS_HOST']}:{values['REDIS_PORT']}/{values['REDIS_DB']}"

    class Config:
        env_file = ".env"

settings = Settings()
settings.REDIS_URL = settings.assemble_redis_connection(settings.model_dump())
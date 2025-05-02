from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    NEURAL_HOST: str = Field(..., min_length=1)
    NEURAL_PORT: int = Field(..., ge=1, le=65535)
    APP_DEBUG: bool = False

    POSTGRES_HOST: str = Field(..., min_length=1)
    POSTGRES_PORT: int = Field(..., ge=1, le=65535)
    POSTGRES_USERNAME: str = Field(..., min_length=1)
    POSTGRES_PASSWORD: str = Field(..., min_length=1)
    POSTGRES_DB: str = Field(..., min_length=1)
    POSTGRES_URL: Optional[str] = None

    MINIO_URL: str = Field(..., min_length=1)
    MINIO_ACCESS_KEY: str = Field(..., min_length=1)
    MINIO_SECRET_KEY: str = Field(..., min_length=1)
    MINIO_SECURE: bool = False
    MINIO_BUCKET_AUDIO: str = Field(..., min_length=1)

    AUTH_SERVICE_URL: str = Field(..., min_length=1)

    @classmethod
    def assemble_postgres_connection(cls, values: dict) -> str:
        return f"postgresql+asyncpg://{values['POSTGRES_USERNAME']}:{values['POSTGRES_PASSWORD']}@{values['POSTGRES_HOST']}:{values['POSTGRES_PORT']}/{values['POSTGRES_DB']}"

    class Config:
        env_file = ".env"

settings = Settings()
settings.POSTGRES_URL = settings.assemble_postgres_connection(settings.model_dump())
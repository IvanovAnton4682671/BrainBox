from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings): #для загрузки и валидации переменных окружения
    #настройки сервиса
    AUTHORIZATION_HOST: str = Field(..., min_length=1)
    AUTHORIZATION_PORT: int = Field(..., ge=1, le=65535)
    APP_DEBUG: bool = False

    #настройки БД PostgreSQL
    POSTGRES_HOST: str = Field(..., min_length=1)
    POSTGRES_PORT: int = Field(..., ge=1, le=65535)
    POSTGRES_USERNAME: str = Field(..., min_length=1)
    POSTGRES_PASSWORD: str = Field(..., min_length=1)
    POSTGRES_DB: str = Field(..., min_length=1)
    POSTGRES_URL: Optional[str] = None #создание адреса подключения к БД PostgreSQL

    #настройка БД Redis
    REDIS_HOST: str = Field(..., min_length=1)
    REDIS_PORT: int = Field(..., ge=1, le=65535)
    REDIS_DB: int = Field(..., ge=0, le=65535)
    REDIS_URL: Optional[str] = None #создание адреса подключения к БД Redis

    @classmethod
    def assemble_postgres_connection(cls, values: dict) -> str:
        return f"postgresql+asyncpg://{values['POSTGRES_USERNAME']}:{values['POSTGRES_PASSWORD']}@{values['POSTGRES_HOST']}:{values['POSTGRES_PORT']}/{values['POSTGRES_DB']}"

    @classmethod
    def assemble_redis_connection(cls, values: dict) -> str:
        return f"redis://{values['REDIS_HOST']}:{values['REDIS_PORT']}/{values['REDIS_DB']}"

    #указывает на .env-файл и чувствителен к регистру, а также игнорирует лишние переменные
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

#для импорта в другие файлы, а также динамически создаём URL при инициализации
settings = Settings()
settings.POSTGRES_URL = settings.assemble_postgres_connection(settings.model_dump()) #model_dump вместо прямого доступа к __dict__
settings.REDIS_URL = settings.assemble_redis_connection(settings.model_dump())
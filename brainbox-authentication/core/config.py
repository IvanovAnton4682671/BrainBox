from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings): #для загрузки и валидации переменных окружения
    #настройки БД
    POSTGRES_HOST: str = Field(..., min_length=1)
    POSTGRES_PORT: int = Field(..., ge=1, le=65535)
    POSTGRES_USERNAME: str = Field(..., min_length=1)
    POSTGRES_PASSWORD: str = Field(..., min_length=1)
    POSTGRES_DB: str = Field(..., min_length=1)

    #создание адреса подключения к БД
    DATABASE_URL: Optional[str] = None

    @classmethod
    def assemble_db_connection(cls, values: dict) -> str:
        return f"postgresql+asyncpg://{values['POSTGRES_USERNAME']}:{values['POSTGRES_PASSWORD']}@{values['POSTGRES_HOST']}:{values['POSTGRES_PORT']}/{values['POSTGRES_DB']}"

    APP_DEBUG: bool = False

    #указывает на .env-файл и чувствителен к регистру, а также игнорирует лишние переменные
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

#для импорта в другие файлы, а также динамически создаём URL при инициализации
settings = Settings()
settings.DATABASE_URL = settings.assemble_db_connection(settings.model_dump()) #model_dump вместо прямого доступа к __dict__
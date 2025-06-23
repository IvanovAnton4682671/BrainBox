from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings): #для загрузки и валидации переменных окружения
    #настройки БД PostgreSQL
    POSTGRES_URL: str = Field(..., min_length=1)

    #настройка БД Redis
    REDIS_URL: str = Field(..., min_length=1)

    #настройки сервиса
    AUTHORIZATION_HOST: str = Field(..., min_length=1)
    AUTHORIZATION_PORT: int = Field(..., ge=1, le=65535)
    APP_DEBUG: bool = False

    GATEWAY_URL: str = Field(..., min_length=1)

    NEURAL_SERVICE_URL: str = Field(..., min_length=1)

    #указывает на .env-файл
    class Config:
        env_file = ".env"

#для импорта в другие файлы, а также динамически создаём URL при инициализации
settings = Settings()
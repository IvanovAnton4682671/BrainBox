from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    NEURAL_HOST: str = Field(..., min_length=1)
    NEURAL_PORT: int = Field(..., ge=1, le=65535)
    APP_DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
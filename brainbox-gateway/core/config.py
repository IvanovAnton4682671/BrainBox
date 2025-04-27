from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    GATEWAY_HOST: str = Field(..., min_length=1)
    GATEWAY_PORT: int = Field(..., ge=1, le=65535)

    CLIENT_URL: str = Field(..., min_length=1)

    AUTH_SERVICE_URL: str = Field(..., min_length=1)
    NEURAL_SERVICE_URL: str = Field(..., min_length=1)

    class Config:
        env_file = ".env"

settings = Settings()
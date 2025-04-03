from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime

class UserBase(BaseModel):
    """
    Базовая схема с общими полями пользователя
    Не используется напрямую, только для наследования
    """
    email: EmailStr = Field(
        ...,
        description="Уникальная почта пользователя"
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Уникальное имя пользователя",
        pattern=r"^[a-zA-Z0-9]+$"
    )

class UserCreate(UserBase):
    """
    Схема для регистрации нового пользователя
    Добавляет валидацию пароля до хэширования (потому что у пароля сложный паттерн regex)
    """
    password: str = Field(
        ...,
        min_length=5,
        max_length=20,
        description="Пароль пользователя (до хэширования)"
    )

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        """
        Своя валидация пароля
        """
        if not any(c.islower() for c in v):
            raise ValueError("Пароль должен содержать минимум 1 строчную латинскую букву!")
        if not any(c.isupper() for c in v):
            raise ValueError("Пароль должен содержать минимум 1 заглавную латинскую букву!")
        if not any(c.isdigit() for c in v):
            raise ValueError("Пароль должен содержать минимум 1 цифру!")
        if not any(not c.isalnum() for c in v):
            raise ValueError("Пароль должен содержать минимум 1 спецсимвол!")
        return v

class UserResponse(UserBase):
    """
    Схема для ответа API, содержит только безопасные данные
    """
    id: int = Field(
        ...,
        description="ID пользователя"
    )
    created_at: datetime = Field(
        ...,
        description="Дата и время создания записи (UTC)"
    )
    last_login: datetime = Field(
        ...,
        description="Дата и время последнего входа в запись (UTC)"
    )

    class Config:
        from_attributes = True #для совместимости с ORM (бывшее orm_mode)

class UserInDB(UserResponse):
    """
    Внутренняя схема, которая используется только внутри сервиса
    С хэшем пароля
    """
    password_hash: str = Field(
        ...,
        description="Хэш пароля пользователя (bcrypt)"
    )

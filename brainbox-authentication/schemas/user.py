from pydantic import BaseModel, Field, field_validator
from email_validator import validate_email, EmailNotValidError, EmailUndeliverableError
from core.errors import ValidationError
from datetime import datetime
from core.logger import setup_logger

logger = setup_logger("schemas/user.py")

class UserEmail(BaseModel):
    """
    Базовая схема с почтой пользователя
    Не используется напрямую, только для наследования
    """ 
    email: str = Field(
        ...,
        description="Уникальная почта пользователя"
    )

    @field_validator("email")
    def my_validate_email(cls, v: str) -> str:
        """
        Своя валидация почты
        """
        try:
            logger.info(f"Валидация почты: email - {v}")
            if not v or not v.strip():
                logger.warning(f"Почта не может быть пустой: email - {v}")
                raise ValidationError({
                    "code": "empty_email",
                    "message": "Почта не может быть пустой!"
                })
            try:
                validate_email(v)
            except EmailUndeliverableError as e:
                logger.warning(f"Некорректный домен почты: email - {v}")
                raise ValidationError({
                    "code": "invalid_email_domain",
                    "message": "Некорректный домен почты!"
                })
            except EmailNotValidError as e:
                logger.warning(f"Некорректный формат почты: email - {v}")
                raise ValidationError({
                    "code": "invalid_email_format",
                    "message": "Некорректный формат почты!"
                })
            return v
        except Exception as e:
            logger.error(f"Ошибка при валидации email - {v}: {str(e)}", exc_info=True)
            raise

class UserName(BaseModel):
    """
    Базовая схема с именем пользователя
    Не используется напрямую, только для наследования
    """
    name: str = Field(
        ...,
        description="Уникальное имя пользователя",
    )

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        """
        Своя валидация имени
        """
        try:
            logger.info(f"Валидация имени: name - {v}")
            if not v or not v.strip():
                logger.warning(f"Имя не может быть пустым: name - {v}")
                raise ValidationError({
                    "code": "empty_name",
                    "message": "Имя не может быть пустым!"
                })
            if len(v) < 1 or len(v) > 20:
                logger.warning(f"Имя должно быть от 1 до 20 символов: name - {v}")
                raise ValidationError({
                    "code": "invalid_name_length",
                    "message": "Имя должно быть от 1 до 20 символов!"
                })
            if not v.isalnum():
                logger.warning(f"Имя должно содержать только латинские буквы и цифры: name - {v}")
                raise ValidationError({
                    "code": "invalid_name",
                    "message": "Имя должно содержать только латинские буквы и цифры!"
                })
            return v
        except Exception as e:
            logger.error(f"Ошибка при валидации name - {v}: {str(e)}", exc_info=True)
            raise

class UserAuth(UserEmail):
    """
    Схема для авторизации пользователя
    Добавляет валидацию пароля до хэширования (потому что у пароля сложный паттерн regex)
    """
    password: str = Field(
        ...,
        description="Пароль пользователя (до хэширования)"
    )

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        """
        Своя валидация пароля
        """
        try:
            logger.info(f"Валидация пароля.")
            if not v or not v.strip():
                logger.warning(f"Пароль не может быть пустым: password - {v}")
                raise ValidationError({
                    "code": "empty_password",
                    "message": "Пароль не может быть пустым!"
                })
            if len(v) < 5 or len(v) > 20:
                logger.warning(f"Пароль должен быть от 5 до 20 символов: password - {v}")
                raise ValidationError({
                    "code": "invalid_password_length",
                    "message": "Пароль должен быть от 5 до 20 символов!"
                })
            if not any(c.islower() for c in v):
                logger.warning(f"Пароль должен содержать минимум 1 строчную латинскую букву: password - {v}")
                raise ValidationError({
                    "code": "weak_password",
                    "message": "Пароль должен содержать минимум 1 строчную латинскую букву!"
                })
            if not any(c.isupper() for c in v):
                logger.warning(f"Пароль должен содержать минимум 1 заглавную латинскую букву: password - {v}")
                raise ValidationError({
                    "code": "weak_password",
                    "message": "Пароль должен содержать минимум 1 заглавную латинскую букву!"
                })
            if not any(c.isdigit() for c in v):
                logger.warning(f"Пароль должен содержать минимум 1 цифру: password - {v}")
                raise ValidationError({
                    "code": "weak_password",
                    "message": "Пароль должен содержать минимум 1 цифру!"
                })
            if not any(not c.isalnum() for c in v):
                logger.warning(f"Пароль должен содержать минимум 1 спецсимвол: password - {v}")
                raise ValidationError({
                    "code": "weak_password",
                    "message": "Пароль должен содержать минимум 1 спецсимвол!"
                })
            return v
        except Exception as e:
            logger.error(f"Ошибка при валидации пароля: {str(e)}", exc_info=True)
            raise

class UserCreate(UserAuth, UserName):
    """
    Схема для регистрации нового пользователя
    """
    pass

class UserResponse(UserEmail, UserName):
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

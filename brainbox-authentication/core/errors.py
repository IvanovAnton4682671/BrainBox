from functools import wraps
from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError

class ValidationError(RequestValidationError):
    """
    Класс для ошибок валидации (422 Unprocessable Entity)
    """
    pass

class BusinessError(ValueError):
    """
    Класс для бизнес-ошибок (400 Bad Request)
    """
    pass

def error_handler(func):
    """
    Декоратор для отлова ошибок в едином формате
    Используется для ошибок вида:
        { 'code': ..., 'message': ... }
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "success": False,
                    "error": e.args[0]
                }
            )
        except BusinessError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "error": e.args[0]
                }
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "success": False,
                    "error": {
                        "code": "internal_error",
                        "message": "Внутренняя ошибка сервера!"
                    }
                }
            )
    return wrapper
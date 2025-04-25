from functools import wraps
from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

class ValidationError(ValueError):
    """
    Класс для ошибок валидации (422 Unprocessable Entity)
    """
    pass

class BusinessError(ValueError):
    """
    Класс для бизнес-ошибок (400 Bad Request)
    """
    pass

async def handle_request_validation_error(request, exc: RequestValidationError):
    """
    Обработчик ошибок валидации Pydantic, которые FastAPI перехватывает как свои RequestValidationError,
    т.е. обрабатываем ошибки 422 Unprocessable Entity
    Возвращает информацию об ошибке в формате:
        error.response.data.detail:
            success: ...,
            error:
                code: ...,
                message: ...,
    """
    first_error = exc.errors()[0]
    error_msg = first_error.get("msg", "")
    #извлекаем свою структуру из стандартной ошибки FastAPI
    if "Value error, " in error_msg:
        try:
            error_data = eval(error_msg.split("Value error, ")[1])
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "detail": {
                        "success": False,
                        "error": error_data
                    }
                }
            )
        except:
            pass
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": {
                "success": False,
                "error": {
                    "code": "validation_error",
                    "message": str(exc)
                }
            }
        }
    )

def error_handler(func):
    """
    Основной декоратор для возврата ошибок в едином формате
    Возвращает информацию об ошибке в формате:
        error.response.data.detail:
            success: ...,
            error:
                code: ...,
                message: ...,
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
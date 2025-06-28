from core.logger import setup_logger
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routers import authentication
from core.config import settings
import uvicorn
from core.errors import handle_request_validation_error
import time
from databases.redis import redis
from fastapi.exceptions import RequestValidationError
from prometheus_fastapi_instrumentator import Instrumentator

logger = setup_logger("main")

app = FastAPI(
    title="BrainBox Authentication Service",
    description="Сервис аутентификации пользователей проекта BrainBox"
)

#настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.GATEWAY_URL, settings.NEURAL_SERVICE_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#подключение роутера
app.include_router(authentication.router)

#дополнительный обработчик ошибок
app.add_exception_handler(RequestValidationError, handle_request_validation_error)

@app.middleware("http")
async def log_request(request: Request, call_next):
    """
    Метод для логирования всех http-запросов
    """
    start_time = time.time()
    logger.info(f"Получили запрос: {request.method} {request.url}")
    try:
        sessionid = request.cookies.get("sessionid")
        logger.info(f"Получили sessionid = {sessionid}")
        if sessionid:
            user_id = await redis.get(f"session:{sessionid}")
            if not user_id:
                response = Response(status_code=401)
                response.delete_cookie("sessionid")
                process_time = (time.time() - start_time) * 1000
                logger.warning(
                    f"Не получили user_id по session_id: {request.method} {request.url}"
                    f" Статус: {response.status_code}"
                    f" Время: {process_time:.2f}мс"
                )
                return response
            logger.info(f"Получили user_id = {user_id}")
            request.state.user_id = int(user_id)
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"Ответ: {request.method} {request.url}"
            f" Статус: {response.status_code}"
            f" Время: {process_time:.2f}мс"
        )
        return response
    except Exception as e:
        process_time = (time.time() - start_time) * 1000
        logger.error(
            f"Ошибка запроса: {request.method} {request.url}"
            f" Ошибка: {str(e)}"
            f" Время: {process_time:.2f}мс",
            exc_info=True
        )
        if isinstance(e, HTTPException) and e.status_code == 401:
            response = Response(
                content=f"Auth error: {str(e)}",
                status_code=401
            )
            response.delete_cookie("sessionid")
            return response
        return Response(
            content=f"Internal server error: {str(e)}",
            status_code=500
        )

Instrumentator().instrument(app).expose(app)

@app.get("/")
async def root():
    return {"message": "BrainBox Authentication Service is running..."}

if __name__ == "__main__":
    logger.info("Сервис аутентификации запущен...")
    uvicorn.run("main:app", host=settings.AUTHORIZATION_HOST, port=settings.AUTHORIZATION_PORT, reload=True)
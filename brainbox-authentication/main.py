from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from database.database import create_tables
from fastapi.middleware.cors import CORSMiddleware
from api.routers import authentication
import uvicorn
from core.logger import setup_logger
import time

logger = setup_logger("http")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Создание таблиц при старте (временное решение до Alembic)
    """
    print("Creating tables...")
    await create_tables()
    yield
    print("Shutting down...")

app = FastAPI(
    title="BrainBox Authentication Service",
    description="Сервис аутентификации пользователей проекта BrainBox"
)

#настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#подключение роутера
app.include_router(authentication.router)

@app.middleware("http")
async def log_request(request: Request, call_next):
    """
    Метод для логирования всех http-запросов
    """
    start_time = time.time()
    logger.info(f"Attempt request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"Response: {request.method} {request.url}"
            f" Status: {response.status_code}"
            f" Time: {process_time:.2f}ms"
        )
        return response
    except Exception as e:
        process_time = (time.time() - start_time) * 1000
        logger.error(
            f"Request failed: {request.method} {request.url}"
            f" Error: {str(e)}"
            f" Time: {process_time:.2f}ms",
            exc_info=True
        )
        return Response(
            content=f"Internal server error: {str(e)}",
            status_code=500
        )

@app.get("/")
async def root():
    return {"message": "BrainBox Authentication Service is running..., for help: http://localhost:8001/docs"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
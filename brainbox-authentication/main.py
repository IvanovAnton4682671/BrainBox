from contextlib import asynccontextmanager
from fastapi import FastAPI
from database.database import create_tables
from fastapi.middleware.cors import CORSMiddleware
from api.routers import authentication
import uvicorn

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

@app.get("/")
async def root():
    return {"message": "BrainBox Authentication Service is running..., for help: http://localhost:8001/docs"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
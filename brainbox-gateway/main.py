from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.logger import setup_logger
from routers import audio, auth, text, image
from core.task_listener import task_listener
import asyncio
import uvicorn
from core.rabbitmq import rabbitmq
from contextlib import asynccontextmanager

logger = setup_logger("http")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbitmq.connect()
    listener_task = asyncio.create_task(task_listener.start())
    yield
    await task_listener.stop()
    await listener_task
    await rabbitmq.close()

app = FastAPI(
    title="BrainBox API Gateway",
    description="API Gateway-узел проекта BrainBox",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CLIENT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(audio.router)
app.include_router(image.router)
app.include_router(text.router)

@app.get("/")
async def root():
    return {"message": "BrainBox API Gateway is running..."}

if __name__ == "__main__":
    logger.info("API Gateway запущен!")
    uvicorn.run("main:app", host=settings.GATEWAY_HOST, port=settings.GATEWAY_PORT, reload=True)
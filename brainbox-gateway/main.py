from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.logger import setup_logger
from routers import audio, auth, text, image
from core.task_listener import task_listener
import asyncio
import uvicorn
from core.rabbitmq import rabbitmq
from contextlib import asynccontextmanager
from core.ws_manager import ws_connection_manager
from databases.redis import redis
import json

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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint для клиентских уведомлений
    """

    logger.warning("ПРобуем установить соединение с клиентом")
    connected = await ws_connection_manager.connect(websocket)
    if not connected:
        logger.warning("соединение отсутствует, дальше работать невозможно")
        return
    logger.warning("соединение установлено!")
    session_id = websocket.cookies.get("sessionid")
    logger.warning(f"получили session_id = {session_id}")
    pending_keys = await redis.keys(f"ws_pending:{session_id}:*")
    logger.warning(f"получили pending_keys = {pending_keys}")
    for key in pending_keys:
        message = json.loads(await redis.get(key))
        logger.warning(f"пробуем отправить message = {message}")
        await websocket.send_json(message)
        await redis.delete(key)
    try:
        while True:
            data = await websocket.receive_text()
            if data != "ping":
                logger.warning(f"Получены некорректные данные от WebSocket: {data}")
    except WebSocketDisconnect:
        await ws_connection_manager.disconnect(session_id)
        logger.warning(f"Произошло отсоединение от WebSocket для session_id = {session_id}")

if __name__ == "__main__":
    logger.info("API Gateway запущен!")
    uvicorn.run("main:app", host=settings.GATEWAY_HOST, port=settings.GATEWAY_PORT, reload=True)
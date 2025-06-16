import asyncio
from fastapi import WebSocket
from starlette.websockets import WebSocketState
from core.logger import setup_logger
from databases.redis import redis
import json

logger = setup_logger("core/ws_manager.py")

class WSConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.lock = asyncio.Lock()

    async def authenticate(self, websocket: WebSocket) -> str:
        """
        Аутентификация по sessionid из кук
        """

        logger.warning(f"Пробуем аутентифицироваться")
        session_id = websocket.cookies.get("sessionid")
        logger.warning(f"Получили такой session_id = {session_id}")
        if not session_id:
            logger.warning(f"session_id отсутствует, закрываем соединение")
            await websocket.close(code=1008)
            return None
        logger.warning(f"session_id = {session_id} есть, работаем дальше")
        user_id = await redis.get(f"session:{session_id}")
        if not user_id:
            logger.warning(f"user_id не получили, закрываем соединение")
            await websocket.close(code=1008)
            return None
        logger.warning(f"user_id = {user_id}, работаем дальше!")
        return session_id

    async def connect(self, websocket: WebSocket):
        """
        Принятие нового соединения
        """
        session_id = await self.authenticate(websocket)
        if not session_id:
            return False
        async with self.lock:
            if session_id in self.active_connections:
                logger.warning(f"Session {session_id} already has an active connection")
                return False
            await websocket.accept()
            self.active_connections[session_id] = websocket
            logger.warning(f"WebSocket connected for session: {session_id}")
            return True

    async def disconnect(self, session_id: str):
        """
        Закрытие соединения
        """

        async with self.lock:
            if session_id in self.active_connections:
                del self.active_connections[session_id]
                logger.info(f"WebSocket disconnected for session: {session_id}")

    async def send_message(self, message: dict, session_id: str):
        """
        Отправка сообщения конкретному клиенту
        """

        async with self.lock:
            logger.warning(f"Получили для отправки message = {message} и session_id = {session_id}")
            if session_id in self.active_connections:
                logger.warning("session_id есть в self.active_connection")
                websocket = self.active_connections[session_id]
                if websocket.client_state == WebSocketState.CONNECTED:
                    logger.warning("websocket клиент является законнекченным")
                    try:
                        await websocket.send_json(message)
                        logger.warning("отправили сообщение!")
                        return True
                    except Exception as e:
                        logger.error(f"WebSocket send error: {str(e)}")
                        await self.disconnect(session_id)
            logger.warning("session_id нет в self.active_connection")
            return False

ws_connection_manager = WSConnectionManager()
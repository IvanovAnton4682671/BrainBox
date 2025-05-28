from core.logger import setup_logger
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from core.config import settings
import dramatiq
from databases.postgresql import async_session_maker
from databases.redis import redis
from interfaces.auth import auth_interface
from services.audio import AudioService
from services.text import TextService
from services.image import ImageService
from schemas.image import ImageMessageRequest
import asyncio
import json
from dramatiq import Message
from datetime import datetime
from pydantic import BaseModel, Field

logger = setup_logger("worker.py")

class TempWrapper(BaseModel):
    image_uid: str = Field(
        ...,
        description="Временная обёртка для image_uid"
    )

broker = RabbitmqBroker(url=settings.RABBITMQ_URL)
dramatiq.set_broker(broker)

async def _process_task_result(task_id: str, result: dict, response_queue: str):
    """
    Общая функция для сохранения результатов и отправки ответов
    """
    def json_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Тип {type(obj)} некорректный!")
    print(result)
    queue_type = str(response_queue.split("_")[0])
    await redis.setex(
        name=f"{queue_type}_task_result:{task_id}",
        time=3600,
        value=json.dumps(result.model_dump(), default=json_serializer)
        #value=json.dumps(result.model_dump())
    )
    message = Message(
        queue_name=response_queue,
        actor_name=f"handle_{queue_type}_result",
        args=[task_id],
        kwargs={"status": "completed"},
        options={}
    )
    broker.enqueue(message)

@dramatiq.actor(queue_name=settings.RABBITMQ_AUDIO_REQUESTS)
def process_audio_task(task_id: str, *, session_id: str, audio_uid: str):
    """
    Обработчик аудио-задач. Получает:
        task_id как позиционный аргумент
        session_id, audio_uid как именованные аргументы
    """
    async def async_task():
        try:
            #создаём новый event loop если нужно
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                asyncio.set_event_loop(asyncio.new_event_loop())
            async with async_session_maker() as session:
                user_id = await auth_interface.get_user_id(session_id)
                audio_service = AudioService(session)
                result = await audio_service.recognize_saved_audio(user_id, audio_uid)
                await _process_task_result(
                    task_id,
                    result,
                    settings.RABBITMQ_AUDIO_RESPONSES
                )
        except Exception as e:
            logger.error(f"Ошибка при выполнении аудио-задачи: {str(e)}", exc_info=True)
            raise
    asyncio.run(async_task())

@dramatiq.actor(queue_name=settings.RABBITMQ_TEXT_REQUESTS)
def process_text_task(task_id: str, *, session_id: str, message_text: str):
    """
    Обработчик текстовых задач. Получает:
        task_id как позиционный аргумент
        session_id, message_text как именованные аргументы
    """
    async def async_task():
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                asyncio.set_event_loop(asyncio.new_event_loop())
            async with async_session_maker() as session:
                user_id = await auth_interface.get_user_id(session_id)
                text_service = TextService(session)
                result = await text_service.create_answer(user_id, message_text)
                await _process_task_result(
                    task_id,
                    result,
                    settings.RABBITMQ_TEXT_RESPONSES
                )
        except Exception as e:
            logger.error(f"Ошибка при выполнении текстовой задачи: {str(e)}", exc_info=True)
            raise
    asyncio.run(async_task())

@dramatiq.actor(queue_name=settings.RABBITMQ_IMAGE_REQUESTS)
def process_image_task(task_id: str, *, session_id: str, message_text: str):
    """
    Обработчик задач по генерации картинок. Получает:
        task_id как позиционный аргумент
        session_id, message_text как именованные аргументы
    """
    async def async_task():
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                asyncio.set_event_loop(asyncio.new_event_loop())
            async with async_session_maker() as session:
                user_id = await auth_interface.get_user_id(session_id)
                image_service = ImageService(session)
                user_message = ImageMessageRequest(
                    user_id=user_id,
                    message_text=message_text
                )
                result = await image_service.create_answer(user_message)
                await _process_task_result(
                    task_id=task_id,
                    result=TempWrapper(image_uid=str(result.image_uid)),
                    response_queue=settings.RABBITMQ_IMAGE_RESPONSES
                )
        except Exception as e:
            logger.error(f"Ошибка выполнения задачи по генерации картинки: {str(e)}", exc_info=True)
            raise
    asyncio.run(async_task())

@dramatiq.actor(queue_name=settings.RABBITMQ_AUDIO_RESPONSES)
def handle_audio_result(task_id: str, *, status: str):
    logger.info(f"Аудио-задача {task_id} завершена со статусом {status}")

@dramatiq.actor(queue_name=settings.RABBITMQ_TEXT_RESPONSES)
def handle_text_result(task_id: str, *, status: str):
    logger.info(f"Текстовая задача {task_id} завершена со статусом {status}")

@dramatiq.actor(queue_name=settings.RABBITMQ_IMAGE_RESPONSES)
def handle_image_result(task_id: str, *, status: str):
    logger.info(f"Задача по генерации картинки {task_id} завершена со статусом {status}")
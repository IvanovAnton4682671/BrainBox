from core.logger import setup_logger
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from core.config import settings
import dramatiq
from databases.postgres import async_session_maker
from databases.redis import redis
from interfaces.auth import auth_service
from services.audio import AudioService
import asyncio
import json
from dramatiq import Message

logger = setup_logger("worker.py")

broker = RabbitmqBroker(url=settings.RABBITMQ_URL)
dramatiq.set_broker(broker)

@dramatiq.actor(queue_name=settings.RABBITMQ_AUDIO_REQUESTS)
def process_audio_task(task_id: str, *, session_id: str, audio_uid: str):
    """
    Обработчик задач. Получает:
        task_id как позиционный аргумент
        session_id, audio_uid как именованные аргументы
    """
    async def async_task():
        async with async_session_maker() as db:
            try:
                user_id = await auth_service.get_user_id(session_id)
                audio_service = AudioService(db)
                result = await audio_service.recognize_saved_audio(user_id, audio_uid)
                await redis.setex(
                    name=f"audio_task_result:{task_id}",
                    time=3600,
                    value=json.dumps(result.model_dump())
                )
                message = Message(
                    queue_name=settings.RABBITMQ_AUDIO_RESPONSES,
                    actor_name="handle_audio_result",
                    args=[task_id],
                    kwargs={ "status": "completed" },
                    options={}
                )
                broker.enqueue(message)
            except Exception as e:
                logger.error(f"Ошибка при выполнении задачи воркером: {str(e)}", exc_info=True)
                raise
    asyncio.run(async_task())

@dramatiq.actor(queue_name=settings.RABBITMQ_AUDIO_RESPONSES)
def handle_audio_result(task_id: str, *, status: str):
    logger.info(f"Задача {task_id} завершена со статусом {status}")
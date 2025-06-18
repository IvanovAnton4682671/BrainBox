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
import json
from dramatiq import Message
from datetime import datetime
from pydantic import BaseModel, Field
from dramatiq.middleware.asyncio import AsyncIO

logger = setup_logger("worker.py")

class TempWrapper(BaseModel):
    image_uid: str = Field(
        ...,
        description="Временная обёртка для image_uid"
    )

    def to_dict(self):
        return {"image_uid": self.image_uid}

broker = RabbitmqBroker(url=settings.RABBITMQ_URL)
broker.add_middleware(AsyncIO())
dramatiq.set_broker(broker)

@dramatiq.actor(queue_name=settings.RABBITMQ_AUDIO_REQUESTS)
async def process_audio_task(task_id: str, *, session_id: str, audio_uid: str):
    """
    Обработчик аудио-задач. Получает:
        task_id как позиционный аргумент
        session_id, audio_uid как именованные аргументы
    """

    try:
        async with async_session_maker() as session:
            try:
                user_id = await auth_interface.get_user_id(session_id)
                audio_service = AudioService(session)
                result = await audio_service.recognize_saved_audio(user_id, audio_uid)
                logger.warning(f"Задача {task_id} отработана с результатом {result}")
                redis_key = f"audio_task_result:{task_id}"
                await redis.setex(
                    name=redis_key,
                    time=3600,
                    value=json.dumps(result.to_dict())
                )
                logger.warning(f"Задача {task_id} сохранена в redis по {redis_key}")
            except Exception as e:
                await session.rollback()
                raise
            finally:
                await session.close()
    except Exception as e:
        raise

@dramatiq.actor(queue_name=settings.RABBITMQ_TEXT_REQUESTS)
async def process_text_task(task_id: str, *, session_id: str, message_text: str):
    """
    Обработчик текстовых задач. Получает:
        task_id как позиционный аргумент
        session_id, message_text как именованные аргументы
    """

    try:
        async with async_session_maker() as session:
            try:
                user_id = await auth_interface.get_user_id(session_id)
                text_service = TextService(session)
                result = await text_service.create_answer(user_id, message_text)
                logger.warning(f"Задача {task_id} отработана с результатом {result}")
                redis_key = f"text_task_result:{task_id}"
                await redis.setex(
                    name=redis_key,
                    time=3600,
                    value=json.dumps(result.to_dict())
                )
                logger.warning(f"Задача {task_id} сохранена в redis по {redis_key}")
            except Exception as e:
                await session.rollback()
                raise
            finally:
                await session.close()
    except Exception as e:
        raise

@dramatiq.actor(queue_name=settings.RABBITMQ_IMAGE_REQUESTS)
async def process_image_task(task_id: str, *, session_id: str, message_text: str):
    """
    Обработчик задач по генерации картинок. Получает:
        task_id как позиционный аргумент
        session_id, message_text как именованные аргументы
    """

    try:
        async with async_session_maker() as session:
            try:
                user_id = await auth_interface.get_user_id(session_id)
                image_service = ImageService(session)
                user_message = ImageMessageRequest(
                    user_id=user_id,
                    message_text=message_text
                )
                result = await image_service.create_answer(user_message)
                wrapped_result = TempWrapper(image_uid=str(result.image_uid))
                logger.warning(f"Задача {task_id} отработана с результатом {wrapped_result}")
                redis_key = f"image_task_result:{task_id}"
                await redis.setex(
                    name=redis_key,
                    time=3600,
                    value=json.dumps(wrapped_result.to_dict())
                )
                logger.warning(f"Задача {task_id} сохранена в redis по {redis_key}")
            except Exception as e:
                await session.rollback()
                raise
            finally:
                await session.close()
    except Exception as e:
        raise
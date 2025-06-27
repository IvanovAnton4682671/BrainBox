from core.logger import setup_logger
import uuid
from databases.redis import redis
from core.rabbitmq import rabbitmq
from core.config import settings
import json

logger = setup_logger("interfaces.audio_tasks")

async def create_audio_task(session_id: str, audio_uid: str) -> str:
    task_id = str(uuid.uuid4())
    #сохраняем в Redis на час
    await redis.setex(
        name=f"audio_task:{task_id}",
        time=3600,
        value=json.dumps({
            "session_id": session_id,
            "audio_uid": audio_uid
        })
    )
    logger.info(f"Сохранили задачу task_id = {task_id} в redis")
    task_data = {
        "actor_name": "process_audio_task",
        "queue_name": f"{settings.RABBITMQ_AUDIO_REQUESTS}",
        "args": [task_id],
        "kwargs": {
            "session_id": session_id,
            "audio_uid": audio_uid
        },
        "options": {"retry_limit": 3}
    }
    #отправляем в RabbitMQ
    await rabbitmq.publish(
        queue_name=settings.RABBITMQ_AUDIO_REQUESTS,
        message=task_data
    )
    logger.info(f"Отправили задачу task_data = {task_data} в очередь {settings.RABBITMQ_AUDIO_REQUESTS}")
    return task_id

async def get_audio_task_result(task_id: str) -> dict:
    result = await redis.get(f"audio_task_result:{task_id}")
    return { "status": "completed", "result": json.loads(result) } if result else { "status": "processing" }
import uuid
from databases.redis import redis
import json
from core.config import settings
from core.rabbitmq import rabbitmq

async def create_image_task(session_id: str, message_text: str):
    task_id = str(uuid.uuid4())
    await redis.setex(
        name=f"image_task:{task_id}",
        time=3600,
        value=json.dumps({
            "session_id": session_id,
            "message_text": message_text
        })
    )
    task_data = {
        "actor_name": "process_image_task",
        "queue_name": f"{settings.RABBITMQ_IMAGE_REQUESTS}",
        "args": [task_id],
        "kwargs": {
            "session_id": session_id,
            "message_text": message_text
        },
        "options": {"retry_limit": 3}
    }
    await rabbitmq.publish(
        queue_name=settings.RABBITMQ_IMAGE_REQUESTS,
        message=task_data
    )
    return task_id

async def get_image_task_result(task_id: str) -> dict:
    result = await redis.get(f"image_task_result:{task_id}")
    return {"status": "completed", "result": json.loads(result)} if result else {"status": "processing"}
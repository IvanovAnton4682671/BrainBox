from core.logger import setup_logger
import json
from databases.redis import redis
import pika
from core.config import settings
import threading

logger = setup_logger("core/task_listener.py")

def _listen_for_results():
    def callback(ch, method, properties, body):
        try:
            data = json.loads(body)
            task_id = data["task_id"]
            result = data["result"]
            redis.setex(
                name=f"audio_task_result:{task_id}",
                time=3600,
                value=json.dumps(result)
            )
            logger.info(f"Результат задачи {task_id} сохранён")
        except Exception as e:
            logger.error(f"Ошибка обработки результата: {str(e)}", exc_info=True)
    try:
        connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
        channel = connection.channel()
        channel.queue_declare(queue=settings.RABBITMQ_AUDIO_RESPONSES)
        channel.basic_consume(
            queue=settings.RABBITMQ_AUDIO_RESPONSES,
            on_message_callback=callback,
            auto_ack=True
        )
        logger.info("Слушатель RabbitMQ запущен!")
        channel.start_consuming()
    except Exception as e:
        logger.critical(f"Слушатель упал: {str(e)}", exc_info=True)
        raise

def start_listener_in_background():
    """Запускает слушатель в фоновом потоке"""
    thread = threading.Thread(
        target=_listen_for_results,
        daemon=True,
        name="RabbitMQListener"
    )
    thread.start()
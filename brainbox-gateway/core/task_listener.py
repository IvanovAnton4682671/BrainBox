import pika.exceptions
from core.logger import setup_logger
import json
from databases.redis import redis
import pika
from core.config import settings
import threading
import time

logger = setup_logger("core/task_listener.py")

async def _handle_message(body: bytes, queue_type: str):
    try:
        data = json.loads(body)
        task_id = data["task_id"]
        result = data["result"]
        redis_key = f"{queue_type}_task_result:{task_id}"
        await redis.setex(
            name=redis_key,
            time=3600,
            value=json.dumps(result)
        )
        logger.info(f"Результат задачи {task_id} сохранён в {redis_key}")
    except Exception as e:
        logger.error(f"Ошибка при получении сообщения: {str(e)}", exc_info=True)
        raise

def _listen_for_results():
    def callback(ch, method, properties, body, queue_type):
        _handle_message(body, queue_type.split("_")[0])
    while True:
        connection = None
        try:
            connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
            channel = connection.channel()
            #объявляем и слушаем все очереди
            for queue in [settings.RABBITMQ_AUDIO_RESPONSES, settings.RABBITMQ_TEXT_RESPONSES, settings.RABBITMQ_IMAGE_RESPONSES]:
                try:
                    channel.queue_declare(
                        queue=queue,
                        passive=True
                    )
                except pika.exceptions.ChannelClosedByBroker as e:
                    channel.queue_declare(
                        queue=queue,
                        durable=True
                    )
                channel.basic_consume(
                        queue=queue,
                        on_message_callback=lambda ch, method, properties, body, q=queue: callback(ch, method, properties, body, q),
                        auto_ack=True
                    )
            logger.info("Слушатель RabbitMQ запущен!")
            try:
                channel.start_consuming()
            except pika.exceptions.ConnectionClosedByBroker as e:
                logger.error(f"Соединение разорвано брокером: {str(e)}", exc_info=True)
                raise
            except Exception as e:
                logger.error(f"Ошибка потребления: {str(e)}", exc_info=True)
                raise
        except Exception as e:
            logger.error(f"Ошибка в слушателе: {str(e)}. Переподключаемся...", exc_info=True)
            if connection and connection.is_open:
                try:
                    connection.close()
                except:
                    pass
            #пауза перед повторной попыткой
            time.sleep(5)

def start_listener_in_background():
    """
    Запускает слушатель в фоновом потоке
    """
    thread = threading.Thread(
        target=_listen_for_results,
        name="RabbitMQListener",
        daemon=True
    )
    thread.start()
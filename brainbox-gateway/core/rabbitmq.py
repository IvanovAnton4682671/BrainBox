import pika
from core.config import settings
from core.logger import setup_logger
import json

logger = setup_logger("core/rabbitmq.py")

class RabbitMQ:
    def __init__(self):
        self.connection = None
        self.channel = None

    def connect(self) -> None:
        logger.info("Подключение к RabbitMQ...")
        try:
            self.connection = pika.BlockingConnection(
                pika.URLParameters(
                    settings.RABBITMQ_URL
                )
            )
            self.channel = self.connection.channel()
            logger.info("Подключение установлено!")
        except Exception as e:
            logger.error(f"Ошибка при подключении к RabbitMQ: {str(e)}", exc_info=True)
            raise

    def close(self) -> None:
        logger.info("Отключение от RabbitMQ...")
        try:
            if self.connection and self.connection.is_open:
                self.connection.close()
                logger.info("Отключение произошло!")
        except Exception as e:
            logger.error(f"Ошибка при отключении от RabbitMQ: {str(e)}", exc_info=True)
            raise

    def publish(self, queue_name: str, message: dict) -> None:
        logger.info(f"Попытка опубликовать сообщение message - {message} в очередь queue_name - {queue_name}...")
        try:
            if not self.connection or self.connection.is_closed:
                self.connect()
            self.channel.queue_declare(
                queue=f"{queue_name}.XQ",
                durable=True,
                arguments={
                    "x-message-ttl": int(604800000)
                }
            )
            self.channel.queue_declare(
                queue=queue_name,
                durable=True,
                arguments={
                    "x-dead-letter-exchange": "",
                    "x-dead-letter-routing-key": f"{queue_name}.XQ"
                }
            )
            self.channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type='application/json'
                )
            )
            logger.info("Сообщение успешно опубликовано!")
        except Exception as e:
            logger.error(f"Произошла ошибка при публикации сообщения: {str(e)}", exc_info=True)
            self.close()
            raise

rabbitmq = RabbitMQ()
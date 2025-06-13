from core.logger import setup_logger
from typing import Optional
import pika
from pika.adapters.blocking_connection import BlockingChannel
import threading
from core.config import settings
import time
import json

logger = setup_logger("core/rabbitmq.py")

class RabbitMQ:
    def __init__(self):
        self._connection: Optional[pika.BlockingConnection] = None
        self._channel: Optional[BlockingChannel] = None
        self._connection_lock = threading.Lock()
        self._heartbeat_thread: Optional[threading.Thread] = None
        self._running = False

    def _declare_queues(self) -> None:
        """
        Объявляет все необходимые очереди при подключении
        """
        queues = [
            settings.RABBITMQ_AUDIO_REQUESTS,
            settings.RABBITMQ_AUDIO_RESPONSES,
            settings.RABBITMQ_IMAGE_REQUESTS,
            settings.RABBITMQ_IMAGE_RESPONSES,
            settings.RABBITMQ_TEXT_REQUESTS,
            settings.RABBITMQ_TEXT_RESPONSES
        ]
        logger.info("Создаём очереди...")
        for queue in queues:
            try:
                self._channel.queue_declare(
                    queue=f"{queue}.XQ",
                    durable=True,
                    arguments={"x-message-ttl": int(604800000)}
                )
                self._channel.queue_declare(
                    queue=queue,
                    durable=True,
                    arguments={
                        "x-dead-letter-exchange": "",
                        "x-dead-letter-routing-key": f"{queue}.XQ"
                    }
                )
                self._channel.queue_declare(
                    queue=f"{queue}.DQ",
                    durable=True,
                    arguments={
                        "x-dead-letter-exchange": "",
                        "x-dead-letter-routing-key": f"{queue}.XQ"
                    }
                )
            except Exception as e:
                logger.error(f"Ошибка при создании очередей: {str(e)}", exc_info=True)
                raise
        logger.info("Очереди успешно созданы!")

    def _connect(self) -> None:
        """
        Установка соединения с RabbitMQ
        """
        with self._connection_lock:
            if self._connection and self._connection.is_open:
                return
            try:
                logger.info("Устанавливаем соединение с RabbitMQ...")
                self._connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
                self._channel = self._connection.channel()
                self._declare_queues()
                logger.info("Соединение установлено!")
            except Exception as e:
                logger.error(f"Ошибка при подключении к RabbitMQ: {str(e)}", exc_info=True)
                self._connection = None
                self._channel = None
                raise

    def _close_connection(self) -> None:
        """
        Отключение от RabbitMQ
        """
        with self._connection_lock:
            if self._connection and self._connection.is_open:
                try:
                    self._connection.close()
                except Exception as e:
                    logger.error(f"Ошибка при отключении от RabbitMQ: {str(e)}", exc_info=True)
                finally:
                    self._connection = None
                    self._channel = None

    def _start_heartbeat(self) -> None:
        """
        Запускает поток для проверки соединения
        """
        def heartbeat():
            while self._running:
                try:
                    logger.info("Попытка Heartbeat проверки...")
                    with self._connection_lock:
                        if not self._connection or self._connection.is_closed:
                            self._connect()
                        elif self._channel and self._channel.is_closed:
                            self._channel = self._connection.channel()
                except Exception as e:
                    logger.warning(f"Heartbeat проверка не удалась: {str(e)}", exc_info=True)
                time.sleep(30)
        self._heartbeat_thread = threading.Thread(
            target=heartbeat,
            name="RabbitMQHeartbeat",
            daemon=True
        )
        self._heartbeat_thread.start()

    def start(self) -> None:
        """
        Запускает фоновое соединение и Heartbeat
        """
        self._running = True
        self._connect()
        self._start_heartbeat()

    def stop(self) -> None:
        """
        Останавливает соединение и Heartbeat
        """
        self._running = False
        if self._heartbeat_thread:
            self._heartbeat_thread.join()
        self._close_connection()

    def publish(self, queue_name: str, message: dict) -> None:
        """
        Публикует сообщение в очередь
        """
        attempts = 0
        max_attempts = 3
        while attempts < max_attempts:
            try:
                with self._connection_lock:
                    if not self._connection or self._connection.is_closed:
                        self._connect()
                    if not self._channel or self._channel.is_closed:
                        self._channel = self._connection.channel()
                    self._channel.basic_publish(
                        exchange="",
                        routing_key=queue_name,
                        body=json.dumps(message),
                        properties=pika.BasicProperties(
                            delivery_mode=2,
                            content_type="application/json"
                        )
                    )
                    logger.info(f"Сообщение {message} отправлено в очередь {queue_name}!")
                    return
            except Exception as e:
                time.sleep(1)
                self.stop()
                self.start()
                #attempts += 1
                #logger.error(f"Ошибка при публикации сообщения: {str(e)}", exc_info=True)
                #if attempts < max_attempts:
                    #time.sleep(1)
                    #self._close_connection()
                #else:
                    #raise RuntimeError(f"Не удалось отправить сообщение после {max_attempts} попыток!")

rabbitmq = RabbitMQ()
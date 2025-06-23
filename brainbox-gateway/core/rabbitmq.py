from core.logger import setup_logger
import aio_pika
import asyncio
from core.config import settings
import json

logger = setup_logger("core/rabbitmq.py")

class RabbitMQ:
    def __init__(self):
        self.connection: aio_pika.RobustConnection = None
        self.channel: aio_pika.RobustChannel = None
        self._connection_lock = asyncio.Lock()
        self._queues_declared = False

    async def _declare_queues(self) -> None:
        """
        Асинхронное объявление очередей (идемпотентная операция)
        """

        if self._queues_declared:
            return
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
                #главная очередь с DLQ политикой
                await self.channel.declare_queue(
                    name=queue,
                    durable=True,
                    arguments={
                        "x-dead-letter-exchange": "",
                        "x-dead-letter-routing-key": f"{queue}.XQ"
                    }
                )
                #очередь для повторной обработки (DQ)
                await self.channel.declare_queue(
                    name=f"{queue}.DQ",
                    durable=True,
                    arguments={
                        "x-dead-letter-exchange": "",
                        "x-dead-letter-routing-key": f"{queue}.XQ"
                    }
                )
                #архивная очередь (XQ)
                await self.channel.declare_queue(
                    name=f"{queue}.XQ",
                    durable=True,
                    arguments={"x-message-ttl": int(604800000)}
                )
            except Exception as e:
                logger.error(f"Ошибка при создании очередей: {str(e)}", exc_info=True)
                raise
        logger.info("Очереди успешно созданы!")
        self._declare_queues = True

    async def _on_reconnect(self, connection: aio_pika.RobustConnection) -> None:
        """
        Обработчик автоматического восстановления соединения
        """

        logger.warning("Соединение с RabbitMQ восстановлено после разрыва...")
        self.channel = await connection.channel()
        self._queues_declared = False

    async def connect(self) -> None:
        """
        Установка соединения с автоматическим восстановлением
        """

        async with self._connection_lock:
            if self.connection and not self.connection.is_closed:
                return
            logger.info("Устанавливаем соединение с RabbitMQ...")
            max_attempts = 10
            backoff = 5
            for attempt in range(1, max_attempts + 1):
                try:
                    self.connection = await aio_pika.connect_robust(
                        url=settings.RABBITMQ_URL,
                        timeout=10,
                        client_properties={"connection_name": "gateway-main"},
                        on_reconnect=self._on_reconnect,
                    )
                    self.channel = await self.connection.channel()
                    await self._declare_queues()
                    logger.info("Соединение установлено!")
                    return
                except Exception as e:
                    logger.warning(f"Попытка {attempt}/{max_attempts}: ошибка подключения: {str(e)}")
                    if attempt < max_attempts:
                        await asyncio.sleep(backoff * attempt)
                    else:
                        logger.error(f"Не удалось подключиться после {max_attempts} попыток: {str(e)}", exc_info=True)
                        self.connection = None
                        self.channel = None

    async def close(self) -> None:
        """
        Закрытие соединения
        """

        async with self._connection_lock:
            if self.connection:
                try:
                    await self.connection.close()
                    logger.info("Соединение закрыто!")
                except Exception as e:
                    logger.error(f"Ошибка при закрытии соединения: ", str(e), exc_info=True)
                finally:
                    self.connection = None
                    self.channel = None
                    self._queues_declared = False

    async def ensure_connection(self) -> None:
        """
        Обеспечивает активное соединение
        """

        if not self.connection or self.connection.is_closed:
            await self.connect()

    async def publish(self, queue_name: str, message: dict) -> None:
        """
        Асинхронная публикация сообщения с автоматическим восстановлением
        """

        await self.ensure_connection()
        await self.channel.default_exchange.publish(
            message=aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                content_type="application/json"
            ),
            routing_key=queue_name
        )
        logger.info(f"Сообщение {message} отправлено в очередь {queue_name}...")

rabbitmq = RabbitMQ()
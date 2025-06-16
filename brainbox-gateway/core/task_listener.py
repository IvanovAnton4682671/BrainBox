from core.logger import setup_logger
import aio_pika
import json
from databases.redis import redis
from core.config import settings
from contextlib import suppress
import asyncio
from core.ws_manager import ws_connection_manager

logger = setup_logger("core/task_listener.py")

class TaskListener:
    def __init__(self):
        self.connection: aio_pika.RobustConnection = None
        self.channel: aio_pika.RobustChannel = None
        self._running = False
        self._consuming_tasks = []
        self._reconnect_delay = 3

    async def _handle_message(self, message: aio_pika.IncomingMessage, queue_type: str) -> None:
        """
        Асинхронная обработка входящих сообщений
        """

        try:
            logger.warning(f"Получено сообщение из очереди {queue_type}: {message.body}")
            data = json.loads(message.body.decode())
            if "kwargs" in data:
                task_id = data["kwargs"].get("task_id")
                result = data["kwargs"].get("result")
            else:
                task_id = data.get("task_id")
                result = data.get("result")
            if task_id is None or result is None:
                logger.error(f"Получено сообщение некорректного формата: {message}")
                await message.nack(requeue=False) #отклоняем без повторной очереди
                return
            logger.warning(f"Задача {task_id} обработана с результатом {result}")
            redis_key = f"{queue_type}_task_result:{task_id}"
            await redis.setex(
                name=redis_key,
                time=3600,
                value=json.dumps(result)
            )
            session_id = await redis.get(f"task_session:{task_id}")
            if not session_id:
                logger.error(f"Для задачи {task_id} session_id не найден!")
                await message.ack() #подтверждаем так как обработали
                return
            logger.warning(f"Отправляем уведомление для сессии {session_id}, задача {task_id}")
            if await ws_connection_manager.send_message({
                "type": "task_completed",
                "task_id": task_id,
                "result": result
            }, session_id):
                logger.warning(f"Для задачи {task_id} уведомление отправлено!")
            else:
                logger.warning(f"Не удалось отправить уведомление для задачи {task_id}!")
            logger.warning(f"Результат задачи {task_id} сохранён в {redis_key}")
            await message.ack() #явное подтверждение после успешной обработки
        except Exception as e:
            logger.error(f"Ошибка при обработке сообщения: {str(e)}", exc_info=True)
            await message.nack(requeue=False)

    async def _listen_to_queue(self, queue_name: str) -> None:
        """
        Асинхронное прослушивание одной очереди
        """

        queue_type = queue_name.split("_")[0]
        logger.info(f"Начинается прослушивание очереди {queue_name}...")
        try:
            queue = await self.channel.declare_queue(
                queue_name,
                durable=True,
                passive=True
            )
            async for message in queue:
                await self._handle_message(message, queue_type)
        except aio_pika.exceptions.ChannelClosed:
            logger.warning(f"Канал для очереди {queue_name} закрыт, переподключаемся...")
            raise
        except Exception as e:
            logger.error(f"Ошибка при прослушивании очереди {queue_name}: {str(e)}", exc_info=True)
            raise

    async def _connect(self) -> None:
        """
        Установка соединения с RabbitMQ
        """

        logger.info("Устанавливаем соединение с RabbitMQ...")
        self.connection = await aio_pika.connect_robust(
            url=settings.RABBITMQ_URL,
            client_properties={"connection_name": "gateway-listener"},
            timeout=10
        )
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=10)
        logger.info("Соединение установлено!")

    async def _close(self) -> None:
        """
        Закрытие соединения слушателя
        """

        if self.connection:
            with suppress(Exception):
                await self.connection.close()
                logger.info("Соединение закрыто!")

    async def _start_consume(self) -> None:
        """
        Запуск прослушивания всех очередей
        """

        queues = [
            settings.RABBITMQ_AUDIO_RESPONSES,
            settings.RABBITMQ_IMAGE_RESPONSES,
            settings.RABBITMQ_TEXT_RESPONSES
        ]
        self._consuming_tasks = [asyncio.create_task(self._listen_to_queue(queue)) for queue in queues]
        logger.info("Слушатель запущен!")

    async def start(self) -> None:
        """
        Основной цикл работы слушателя
        """

        self._running = True
        while self._running:
            try:
                await self._connect()
                await self._start_consume()
                await asyncio.gather(*self._consuming_tasks)
            except (aio_pika.exceptions.AMQPConnectionError, ConnectionResetError) as e:
                logger.warning(f"Ошибка соединения: {str(e)}. Переподключаемся через {self._reconnect_delay} сек...")
                await self._close()
                await asyncio.sleep(self._reconnect_delay)
            except asyncio.CancelledError:
                logger.info("Работа слушателя прервана!")
                break
            except Exception as e:
                logger.error(f"Неизвестная ошибка в слушателе: {str(e)}", exc_info=True)
                await self._close()
                await asyncio.sleep(self._reconnect_delay)
            finally:
                for task in self._consuming_tasks:
                    if not task.done():
                        task.cancel()
                        with suppress(asyncio.CancelledError):
                            await task
                self._consuming_tasks = []

    async def stop(self) -> None:
        """
        Остановка слушателя
        """

        self._running = False
        await self._close()

task_listener = TaskListener()
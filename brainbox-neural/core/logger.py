from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

#директория для логов
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

#формат логов
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logger(name: str):
    """
    Базовая настройка логгера
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    #форматтер
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    #консольный вывод
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    #файловый вывод (ротация по 5мб)
    file_handler = RotatingFileHandler(
        LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    #добавляем обработчики
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
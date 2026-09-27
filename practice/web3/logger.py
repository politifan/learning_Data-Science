"""Библиотека для логирования данных в красивом виде"""
import logging
import sys
from pathlib import Path

from colorama import Fore, Style, init


init(autoreset=True)


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, "")

        # Копируем record, чтобы цвет не попал в FileHandler
        colored_record = logging.makeLogRecord(record.__dict__.copy())

        colored_record.levelname = (
            f"{color}{record.levelname}{Style.RESET_ALL}"
        )

        return super().format(colored_record)


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger("app")
    logger.setLevel(level)

    # Чтобы при повторном вызове setup_logging()
    # обработчики не дублировались
    if logger.handlers:
        return logger

    log_format = (
        "%(asctime)s | "
        "%(levelname)-17s | "
        "%(name)s | "
        "%(filename)s:%(lineno)d | "
        "%(message)s"
    )

    # Цветной formatter только для консоли
    console_formatter = ColorFormatter(
        fmt=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Обычный formatter для файла
    file_formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)-8s | "
            "%(name)s | "
            "%(filename)s:%(lineno)d | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)

    # Файл
    file_handler = logging.FileHandler(
        LOG_DIR / "app.log",
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
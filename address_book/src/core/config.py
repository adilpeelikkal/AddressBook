from functools import lru_cache
import logging
import os

from src.core.settings.app import AppSettings
from pathlib import Path

DATABASE_URI = "sqlite:///./sql_app.db"
BASE_DIR = Path(__file__).parent.parent.parent.resolve()


@lru_cache
def get_app_settings() -> AppSettings:
    """
    Return application config.
    """
    return AppSettings(database_url=DATABASE_URI, base_dir=BASE_DIR)


def configure_logging(logger_level=logging.INFO):
    log_dir = os.path.join(BASE_DIR, "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logger_level)

    # Create a file handler for writing logs to a file
    log_file = os.path.join(log_dir, "app.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logger_level)

    # Create a console (terminal) handler for displaying logs in the terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logger_level)

    # Create a formatter for log messages
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

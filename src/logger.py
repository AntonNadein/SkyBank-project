import logging


def setup_logging():
    """Базовая настройка логгера для всего проекта"""
    (
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            filename="..\\logs\\sky_bank.log",  # Запись логов в файл
            filemode="w",  # Перезапись файла при каждом запуске
            encoding="UTF-8",
        )
    )
    return logging.getLogger()

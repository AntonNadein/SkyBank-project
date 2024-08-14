import logging


def setup_logging():
    """Базовая настройка логгера для главной страницы"""
    (
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            filename="..\\logs\\sky_bank_views.log",  # Запись логов в файл
            filemode="w",  # Перезапись файла при каждом запуске
            encoding="UTF-8",
            force=True,
        )
    )
    return logging.getLogger()


def setup_logging_services():
    """Базовая настройка логгера для сервисов"""
    (
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            filename="..\\logs\\sky_bank_services.log",  # Запись логов в файл
            filemode="w",  # Перезапись файла при каждом запуске
            encoding="UTF-8",
            force=True,
        )
    )
    return logging.getLogger()


def setup_logging_services_reports():
    """Базовая настройка логгера для отчетов"""
    (
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            filename="..\\logs\\sky_bank_reports.log",  # Запись логов в файл
            filemode="w",  # Перезапись файла при каждом запуске
            encoding="UTF-8",
            force=True,
        )
    )
    return logging.getLogger()

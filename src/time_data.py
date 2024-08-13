import datetime
import logging

from src.logger import setup_logging

setup_logging()
greeting_by_time_logger = logging.getLogger("func.greeting_by_time")


def greeting_by_time():
    """Функция приветствия в зависимости от времени суток"""
    current_date_time = datetime.datetime.now()
    current_time = current_date_time.strftime("%H:%M")
    greeting_by_time_logger.info(f"Текущее время {current_time}")
    if "06:00" <= str(current_time) < "12:00":
        return "Доброе утро"
    elif "12:00" <= str(current_time) < "18:00":
        return "Добрый день"
    elif "18:00" <= str(current_time) < "22:00":
        return "Добрый вечер"
    elif "22:00" <= str(current_time) < "24:00":
        return "Доброй ночи"
    elif "00:00" <= str(current_time) < "06:00":
        return "Доброй ночи"


# di={}
# tm = greeting_by_time()
# di["greeting"] = tm
# print(di)

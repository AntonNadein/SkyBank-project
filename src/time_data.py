import datetime
import json
import logging
import os
from typing import Optional

from dateutil.relativedelta import relativedelta

from src.constant import PATH_TO_FILE
from src.logger import setup_logging

setup_logging()
datetime_to_time_date_logger = logging.getLogger("func.datetime_to_time_date")
greeting_by_time_logger = logging.getLogger("func.greeting_by_time")
date_first_day_months_logger = logging.getLogger("func.date_first_day_months")
date_per_quarter_logger = logging.getLogger("func.date_per_quarter")


def datetime_to_time_date(file_name: str) -> tuple:
    """
    Принимает на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS возвращает (DD.MM.YYYY, HH:MM)
    """
    with open(os.path.join(PATH_TO_FILE, file_name), "r", encoding="utf-8") as file:
        parsed_data = json.load(file)
        date_time = parsed_data.get("user_date")
        datetime_to_time_date_logger.info(f"На входе: {date_time}")
        if date_time is None:
            str_date_time = None
        else:
            str_date_time = date_time[0]
    if str_date_time is None:
        today = datetime.datetime.now()
    else:
        today = datetime.datetime.strptime(str_date_time, "%Y-%m-%d %H:%M:%S")
    times = today.strftime("%H:%M")
    dates = today.strftime("%d.%m.%Y")
    datetime_to_time_date_logger.info(f"Возвращает: {times}, {dates}")
    return dates, times


def greeting_by_time(times: str = None):
    """Функция приветствия в зависимости от времени суток"""
    if times is None:
        current_date_time = datetime.datetime.now()
    else:
        current_date_time = datetime.datetime.strptime(times, "%H:%M")
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


def date_first_day_months(today: Optional[str] = None) -> tuple:
    """
    Принимает дату в формате DD.MM.YYYY и возвращает первое число месяца
    :param format_date: Опционально: None-текущая дата
    :return: Возвращает первое число месяца
    """
    if today is None:
        today = datetime.datetime.now()
    else:
        today = datetime.datetime.strptime(today, "%d.%m.%Y")
    date_quarter = today.replace(day=1)
    date_first_day_months_logger.info(f"Возвращает: {today}, {date_quarter}")
    return today, date_quarter


def date_per_quarter(format_date: Optional[str] = None) -> tuple:
    """
    Принимает дату в формате DD.MM.YYYY и отнимает 3 месяца
    :param format_date: Опционально: None-текущая дата
    :return:дата минус 3 месяца
    """
    date_per_quarter_logger.info(f"На входе: {format_date}")
    if format_date is None:
        date = datetime.datetime.now()
    else:
        date = datetime.datetime.strptime(format_date, "%d.%m.%Y")
    date_quarter = date - relativedelta(months=3)
    date_per_quarter_logger.info(f"Возвращает: {date}, {date_quarter}")
    return date, date_quarter

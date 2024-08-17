import json
import logging
import os
import re
from typing import Any, Dict, List

from src.constant import PATH_TO_FILE
from src.logger import setup_logging_services

setup_logging_services()
simple_search_logger = logging.getLogger("func.simple_search")
phone_number_search_logger = logging.getLogger("func.phone_number_search")
people_search_logger = logging.getLogger("func.people_search")


def simple_search(file_dict: Dict[str, Any], file_name: str) -> str | List[Dict[str, Any]]:
    """
    Функция простого поиска по описанию
    :param file_dict: list_dict из open_excel файла
    :param file_name: JSON запроса
    :return: JSON-ответ со всеми транзакциями
    """
    list_search = []
    with open(os.path.join(PATH_TO_FILE, file_name), "r", encoding="utf-8") as file:
        parsed_data = json.load(file)
        str_search = parsed_data["user_simple_search"]
        simple_search_logger.info(f"Запрос для поиска: {str_search}")
    for search in file_dict:
        if (str_search).lower() in (search["description"]).lower():
            list_search.append(search)
        elif str_search.lower() in search["category"].lower():
            list_search.append(search)
    simple_search_logger.info(f"Длина результатов поиска: {len(list_search)}")
    return json.dumps(list_search, ensure_ascii=False, indent=4)


def phone_number_search(file_dict: Dict[str, Any]) -> str | List[Dict[str, Any]]:
    """
    Функция всех транзакций по номерам телефонов
    :param file_dict: list_dict из open_excel файла
    :return: JSON-ответ со всеми транзакциями, содержащими в описании мобильные номера
    """
    list_search = []
    pattern = re.compile(r"\d{3}\s\d{3}\W\d{2}\W\d{2}")
    for search_num in file_dict:
        if re.search(pattern, search_num["description"]):
            list_search.append(search_num)
    phone_number_search_logger.info(f"Длина результатов поиска: {len(list_search)}")
    return json.dumps(list_search, ensure_ascii=False, indent=4)


def people_search(file_dict: Dict[str, Any]) -> str | List[Dict[str, Any]]:
    """
    Функция со всеми транзакциями, которые относятся к переводам физлицам
    :param file_dict: list_dict из open_excel файла
    :return:JSON со всеми транзакциями, которые относятся к переводам физлицам
    """
    list_search = []
    pattern = re.compile(r"\b\w+\b\s\w.$")
    for search_num in file_dict:
        if re.search(pattern, search_num["description"]) and "Переводы" in search_num["category"]:
            list_search.append(search_num)
    people_search_logger.info(f"Длина результатов поиска: {len(list_search)}")
    return json.dumps(list_search, ensure_ascii=False, indent=4)

import json
import os
import re
from typing import Any, Dict, List

from src.constant import PATH_TO_FILE
from src.utils import open_excel


def simple_search(file_dict: str, file_name: str) -> str | List[Dict[str, Any]]:
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
    for serch in file_dict:
        if (str_search).lower() in (serch["description"]).lower():
            list_search.append(serch)
        elif str_search.lower() in serch["category"].lower():
            list_search.append(serch)
    return json.dumps(list_search, ensure_ascii=False, indent=4)


# "category": "Пополнения",Перевод с карты
file_open = open_excel("operations.xlsx", output_file="list_dict")
# json_answer = simple_search(file_open, 'user_settings.json')
# print(json_answer)


def phone_number_search(file_dict: str) -> str | List[Dict[str, Any]]:
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
    return json.dumps(list_search, ensure_ascii=False, indent=4)


# МТС Mobile +7 921 999-99-99   \b.+\b\s\S\d\s\d{3}\s\d{3}\W\d{2}\W\d{2}
# json_answer_n = phone_number_search(file_open)
# print(json_answer_n)


def people_search(file_dict: str) -> str | List[Dict[str, Any]]:
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
    return json.dumps(list_search, ensure_ascii=False, indent=4)


# Ybrbnf Y.
# json_answer_s = people_search(file_open)
# print(json_answer_s)

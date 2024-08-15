import json
import logging
import os
from typing import Any, Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import DataFrame

from src.constant import PATH_TO_FILE
from src.logger import setup_logging
from src.time_data import date_first_day_months

load_dotenv()
setup_logging()
open_excel_logger = logging.getLogger("func.open_excel")
request_tickers_logger = logging.getLogger("func.request_tickers")
user_stocks_moex_logger = logging.getLogger("func.user_stocks_moex")
card_info_logger = logging.getLogger("func.card_info")
top_transactions_logger = logging.getLogger("func.top_transactions")


def open_excel(file_name: str, output_file: str = "df") -> List[Dict[str, Any]] | DataFrame | str:
    """
     Преобразовывает excel файл в DataFrame и список словарей
    :param file_name: Имя файла в формате .xlsl
    :param output_file: "df" = DataFrame
                        "list_dict" = List[Dict]
    :return: DataFrame
    """
    open_excel_logger.info(f"Выбор типа выходного файла {output_file}")
    list_dict_excel = []
    try:
        file = os.path.join(PATH_TO_FILE, file_name)
        excel_data = pd.read_excel(file)
        if output_file == "df":
            excel_data.columns = [
                "transaction_date",
                "payment_date",
                "last_digits",
                "status",
                "transaction_amount",
                "transaction_currency",
                "payment_amount",
                "payment_currency",
                "cashback",
                "category",
                "mss",
                "description",
                "bonuses",
                "investment_box",
                "rounding_amount",
            ]
            return excel_data
        elif output_file == "list_dict":
            for index, row in excel_data.iterrows():
                dict_1 = {
                    "index": index,
                    "transaction_date": row.get("Дата операции"),
                    "payment_date": row.get("Дата платежа"),
                    "last_digits": row.get("Номер карты"),
                    "status": row.get("Статус"),
                    "transaction_amount": row.get("Сумма операции"),
                    "transaction_currency": row.get("Валюта операции"),
                    "payment_amount": row.get("Сумма платежа"),
                    "payment_currency": row.get("Валюта платежа"),
                    "cashback": row.get("Кешбэк"),
                    "category": str(row.get("Категория")),
                    "mss": row.get("MCC"),
                    "description": row.get("Описание"),
                    "bonuses": row.get("Бонусы (включая кэшбэк)"),
                    "investment_box": row.get("Округление на инвесткопилку"),
                    "rounding_amount": row.get("Сумма операции с округлением"),
                }
                list_dict_excel.append(dict_1)
            return list_dict_excel
        else:
            return "Укажите тип файла вывода"
    except FileNotFoundError as e:
        open_excel_logger.error(f"Произошла ошибка: {e}")
        return "Файл не найден"


def request_tickers(file_name: str) -> str | List[Dict[str, Any]]:
    """
    Функция конвертации валюты через API
    :param file_name: имя файла
    :return: [{"currency": "USD", "rate": 91.0}]
    """
    list_dict = []
    with open(os.path.join(PATH_TO_FILE, file_name), "r", encoding="utf-8") as file:
        parsed_data = json.load(file)
        list_currencies = parsed_data["user_currencies"]
        request_tickers_logger.info(f"Список данных для поиска: {list_currencies}")
    if list_currencies != []:
        for currency in list_currencies:
            currency_dict = {}
            API_KEY = os.getenv("API_KEY")
            url = f"https://api.apilayer.com/exchangerates_data/" f"convert?to=RUB&from={currency}&amount=1"

            headers = {"apikey": API_KEY}

            response = requests.get(url, headers=headers)
            status_code = response.status_code
            request_tickers_logger.info(f"Статус код {status_code}")

            if status_code != 200:
                return "Нет ответа"

            result = round(response.json()["result"], 2)
            currency_dict["currency"] = currency
            currency_dict["rate"] = result
            list_dict.append(currency_dict)
        return list_dict


def user_stocks_moex(file_name: str) -> List[Dict[str, Any]] | str:
    """
    Функция поиска котировок акций мосбиржи из запроса
    :param file_name: json запрос
    :return: словарь {тикер: цена}
    """
    end_list = []
    with open(os.path.join(PATH_TO_FILE, file_name), "r", encoding="utf-8") as file:
        parsed_data = json.load(file)
        user_stocks_moex_logger.info("Фаийл открыт")
        list_stocks = parsed_data["user_stocks"]
        user_stocks_moex_logger.info(f"Список данных для поиска: {list_stocks}")
    # Запрос на moex биржу
    url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"
    response = requests.get(url)

    status_code = response.status_code
    if status_code != 200:
        return "Нет ответа"

    user_stocks_moex_logger.info(f"Результат ответа сайта: {response}")
    result = response.json()
    # Построение DataFrame для акций
    columns = result["marketdata"]["columns"]
    data = result["marketdata"]["data"]
    df = pd.DataFrame(data=data, columns=columns)
    # Замена индекса тикером акции
    df.set_index("SECID", inplace=True)
    for price in list_stocks:
        price_dict = {"stock": price, "price": float(df.loc[str(price), "WAPRICE"])}
        end_list.append(price_dict)
    return end_list


def card_info(data_frame: DataFrame, date: str) -> List[Dict[str, Any]]:
    """Функция формированя отчета трат и кешбека по картам"""
    list_card_info = []
    list_cashback = []
    date_start, date_end = date_first_day_months(date)
    # фильр даты до начала месяца
    df_filtered_data = data_frame.loc[
        (pd.to_datetime(data_frame.transaction_date, dayfirst=True) <= date_start)
        & (pd.to_datetime(data_frame.transaction_date, dayfirst=True) >= date_end)
    ]
    # отсеять суммы меньше 100 рублей и посчитать кешбек
    df_filtered_status = df_filtered_data[(df_filtered_data.status == "OK") & (df_filtered_data.payment_amount < -100)]
    # создаем индексы для значений payment_amount < 100
    rows_to_update = df_filtered_status.payment_amount < -100
    # заменяем значения payment_amount / 100
    df_filtered_status.loc[rows_to_update, "payment_amount"] = (
        df_filtered_status.loc[rows_to_update, "payment_amount"] / 100
    )
    sum_cashback = df_filtered_status.groupby("last_digits").agg({"payment_amount": "sum"})
    # Получаем список словарей с кэшбеком
    for index, row in sum_cashback.iterrows():
        dict_cashback = {"cashback": round(float(row.get("payment_amount")) * -1)}
        list_cashback.append(dict_cashback)
    card_info_logger.info(f"Список кешбека: {list_cashback}" f"Длинна списка: {len(list_cashback)} ")

    # отсеять и поссумировать пополнения (суммы больше 0 рублей)
    df_filtered = df_filtered_data[(df_filtered_data.status == "OK") & (df_filtered_data.payment_amount < 0)]
    number_sum_cashback = df_filtered.groupby("last_digits").agg({"payment_amount": "sum"})
    # Получаем список словарей с номером карты и тратами
    for index, row in number_sum_cashback.iterrows():
        dict_card = {
            "last_digits": index[1:],
            "payment_amount": round(float(row.get("payment_amount") * -1), 2),
            "cashback": None,
        }
        list_card_info.append(dict_card)
    card_info_logger.info(f"Список карт и расходов: {list_card_info}" f"Длинна списка: {len(list_card_info)} ")

    # слияние списка словарей
    for i in range(len(list_card_info)):
        list_card_info[i].update(list_cashback[i])
    return list_card_info


def top_transactions(data_frame: DataFrame, date) -> List[Dict[str, Any]]:
    """Функция Топ-5 транзакций по сумме платежа"""
    transactions_dict = []
    date_start, first_day = date_first_day_months(date)
    # Фильр успешность операции, платеж(отрицательные)
    # Только операции с картами добавить & (data_frame.last_digits.notnull())
    df_filtered = data_frame.loc[(data_frame.status == "OK") & (data_frame.payment_amount < 0)]
    # Фильр от текущей даты до первого числа месяца
    transactions_by_category_date = df_filtered.loc[
        (pd.to_datetime(df_filtered["transaction_date"], dayfirst=True) <= date_start)
        & (pd.to_datetime(df_filtered["transaction_date"], dayfirst=True) >= first_day)
    ]
    # Сортировка по платежу
    sort_df_payment_amount = transactions_by_category_date.sort_values(by=["payment_amount"])
    top_transactions_logger.info("Сортировка произведена")
    for index, row in sort_df_payment_amount.iterrows():
        dict_card = {
            "amount": float(row.get("payment_amount") * -1),
            "date": row.get("payment_date"),
            "category": row.get("category"),
            "description": row.get("description"),
        }
        transactions_dict.append(dict_card)
    return transactions_dict[:5]

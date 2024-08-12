import json
import os
from typing import List, Dict, Any

import requests
import pandas as pd
from pandas import DataFrame
from dotenv import load_dotenv

from src.constant import PATH_TO_FILE

load_dotenv()


def open_excel(file_name: str, output_file: str = "df") -> List[Dict[str, Any]] | DataFrame | str:
    """
     Преобразовывает excel файл в DataFrame и список словарей
    :param file_name: Имя файла в формате .xlsl
    :param output_file: "df" = DataFrame
                        "list_dict" = List[Dict]
    :return: DataFrame
    """
    list_dict_excel = []
    try:
        file = os.path.join(PATH_TO_FILE, file_name)
        excel_data = pd.read_excel(file)
        if output_file == "df":
            return excel_data
        elif output_file == "list_dict":
            for index, row in excel_data.iterrows():
                dict_1 = {"index": index,
                          "дата_операции": row.get("Дата операции"),
                          "дата_платежа": row.get("Дата платежа"),
                          "номер_карты": row.get("Номер карты"),
                          "статус": row.get("Статус"),
                          "сумма_операции": row.get("Сумма операции"),
                          "валюта_операции": row.get("Валюта операции"),
                          "сумма_платежа": row.get("Сумма платежа"),
                          "валюта_платежа": row.get("Валюта платежа"),
                          "кешбэк": row.get("Кешбэк"),
                          "категория": row.get("Категория"),
                          "мсс": row.get("MCC"),
                          "описание": row.get("Описание"),
                          "бонусы": row.get("Бонусы (включая кэшбэк)"),
                          "инвесткопилка": row.get("Округление на инвесткопилку"),
                          "округление_суммы": row.get("Сумма операции с округлением")
                          }
                list_dict_excel.append(dict_1)
            return list_dict_excel
        else:
            return "Укажите тип файла вывода"
    except FileNotFoundError as e:
        return f"Файл не найден. Ошибка:{e}"


# fil = open_excel("operations.xlsx", "list_dic")
# print(type(fil[0]))
# print(fil[0])


def request_tickers(file_name: str) -> str | List[Dict[str, Any]]:
    '''
    Функция конвертации валюты через API
    :param file_name: имя файла
    :return: [{"currency": "USD", "rate": 91.0}]
    '''
    list_dict = []
    with open(os.path.join(PATH_TO_FILE, file_name), "r", encoding="utf-8") as file:
        parsed_data = json.load(file)
        list_currencies = parsed_data["user_currencies"]
    if list_currencies != []:
        for currency in list_currencies:
            currency_dict = {}
            API_KEY = os.getenv("API_KEY")
            url = (
                f"https://api.apilayer.com/exchangerates_data/"
                f"convert?to=RUB&from={currency}&amount=1"
            )

            headers = {"apikey": API_KEY}

            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                return "Нет ответа"

            result = round(response.json()["result"], 2)
            currency_dict["currency"] = currency
            currency_dict["rate"] = result
            list_dict.append(currency_dict)
        return list_dict


# end_result = request_tickers(("user_settings.json"))
# print(end_result)
# json_data = json.dumps(end_result)
# print(json_data)

def user_stocks_moex(file_name):
    '''
    Функция поиска котировок акций мосбиржи из запроса
    :param file_name: json запрос
    :return: словарь {тикер: цена}
    '''
    with open(os.path.join(PATH_TO_FILE, file_name), "r", encoding="utf-8") as file:
        parsed_data = json.load(file)
        list_stocks = parsed_data["user_stocks"]
    # Запрос на moex биржу
    url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"
    response = requests.get(url)
    result = response.json()
    # Построение DataFrame для акций
    columns = result["marketdata"]["columns"]
    data = result["marketdata"]["data"]
    df = pd.DataFrame(data=data, columns=columns)
    # Замена индекса тикером акции
    df.set_index("SECID", inplace=True)
    price_dict = {}
    for price in list_stocks:
        price_dict[price] = float(df.loc[str(price), "WAPRICE"])
    return price_dict

# da = user_stocks_moex("user_settings.json")
# json_data = json.dumps(da)
# print(json_data)

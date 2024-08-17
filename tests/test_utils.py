import os
from unittest.mock import patch

import pandas as pd
import pytest
from dotenv import load_dotenv
from pandas._testing import assert_frame_equal

from src.utils import card_info, open_excel, request_tickers, top_transactions, user_stocks_moex

load_dotenv()
API_KEY = os.getenv("API_KEY")


@pytest.fixture
def test_category_data():
    """тестовый датафрейм"""
    data = {
        "Дата операции": ["test"],
        "Дата платежа": ["test"],
        "Номер карты": ["test"],
        "Статус": ["test"],
        "Сумма операции": ["test"],
        "Валюта операции": ["test"],
        "Сумма платежа": ["test"],
        "Валюта платежа": ["test"],
        "Кешбэк": ["test"],
        "Категория": ["test"],
        "MCC": ["test"],
        "Описание": ["test"],
        "Бонусы (включая кэшбэк)": ["test"],
        "Округление на инвесткопилку": ["test"],
        "Сумма операции с округлением": ["test"],
    }
    return pd.DataFrame(data, index=[0])


@patch("pandas.read_excel")
def test_read_xlsx_transactions(mock_read_excel, test_category_data):
    """Проверка возвращения списка словарей"""
    file_name = "test.xlsx"
    mock_read_excel.return_value = test_category_data
    result = open_excel(file_name, "list_dict")
    assert result == [
        {
            "bonuses": "test",
            "cashback": "test",
            "category": "test",
            "description": "test",
            "index": 0,
            "investment_box": "test",
            "last_digits": "test",
            "mss": "test",
            "payment_amount": "test",
            "payment_currency": "test",
            "payment_date": "test",
            "rounding_amount": "test",
            "status": "test",
            "transaction_amount": "test",
            "transaction_currency": "test",
            "transaction_date": "test",
        }
    ]


@patch("pandas.read_excel")
def test_read_xlsx_transactions_df(mock_read_excel, test_category_data):
    """Проверка возвращения датафрейма"""
    file_name = "test.xlsx"
    mock_read_excel.return_value = test_category_data
    result_df = open_excel(file_name, "df")
    expected_output = pd.DataFrame(
        [
            {
                "transaction_date": "test",
                "payment_date": "test",
                "last_digits": "test",
                "status": "test",
                "transaction_amount": "test",
                "transaction_currency": "test",
                "payment_amount": "test",
                "payment_currency": "test",
                "cashback": "test",
                "category": "test",
                "mss": "test",
                "description": "test",
                "bonuses": "test",
                "investment_box": "test",
                "rounding_amount": "test",
            }
        ],
        index=[0],
    )
    assert_frame_equal(result_df, expected_output)


def test_read_xlsx_transactions_fail():
    """Проверка наличия файла"""
    file_name = "test.xlsx"
    result_df = open_excel(file_name, "df")
    assert result_df == "Файл не найден"


@patch("json.load")
@patch("requests.get")
def test_request_tickers_201(mocked_response, mock_file):
    """Тест статус кода"""
    mock_file.return_value = {"user_currencies": ["test_1"]}
    mocked_response.return_value.status_code = 201
    result = request_tickers("user_settings.json")
    assert result == "Нет ответа"


@patch("requests.get")
def test_request_tickers(mocked_get):
    """тест нормальной работы"""
    mocked_get.return_value.status_code = 200
    mocked_get.return_value.json.return_value = {"result": 800}
    result = request_tickers("user_settings.json")
    assert result == [{"currency": "USD", "rate": 800}, {"currency": "EUR", "rate": 800}]


@patch("json.load")
@patch("requests.get")
def test_user_stocks_moex_201(mocked_response, mock_file):
    """Тест статус кода"""
    mock_file.return_value = {"user_stocks": ["test_1"]}
    mocked_response.return_value.status_code = 201
    result = user_stocks_moex("user_settings.json")
    assert result == "Нет ответа"


@patch("json.load")
@patch("requests.get")
def test_user_stocks_moex(mocked_get, mock_file):
    """тест нормальной работы"""
    mock_file.return_value = {"user_stocks": ["ABIO"]}
    mocked_get.return_value.status_code = 200
    mocked_get.return_value.json.return_value = {
        "marketdata": {
            "columns": ["SECID", "WAPRICE"],
            "data": [
                [
                    "ABIO",
                    83.52,
                ],
                [
                    "ABRD",
                    227.2,
                ],
            ],
        }
    }
    result = user_stocks_moex("user_settings.json")
    assert result == [{"stock": "ABIO", "price": 83.52}]
    mocked_get.assert_called_once_with(
        "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"
    )


def test_card_info(data_fame_test):
    """тест копии реального файла"""
    result = card_info(data_fame_test, "20.01.2018")
    assert result == [{"last_digits": "1111", "payment_amount": 1025.0, "cashback": 10}]


@pytest.fixture
def test_category_data_sort():
    """тестовый датафрейм"""
    data = {
        "last_digits": ["*1111", "*1111", "*2222", "*3333", "*3333"],
        "transaction_date": [
            "28.07.2018 15:00:00",
            "27.07.2018 15:00:00",
            "25.07.2018 15:00:00",
            "23.07.2018 15:00:00",
            "23.07.2018 15:00:00",
        ],
        "payment_amount": [-1000, -2000, -3000, -3000, 3000],
        "status": ["OK", "OK", "OK", "Failed", "OK"],
    }
    return pd.DataFrame(data, index=[0, 1, 2, 3, 4])


def test_card_info_new_df(test_category_data_sort):
    """тест сортировки и группировки файла"""
    result = card_info(test_category_data_sort, "29.07.2018")
    assert result == [
        {"last_digits": "1111", "payment_amount": 3000.0, "cashback": 30},
        {"last_digits": "2222", "payment_amount": 3000.0, "cashback": 30},
    ]


def test_top_transactions(data_fame_test):
    """тест копии реального файла"""
    result = top_transactions(data_fame_test, "29.07.2018")
    assert result == [{"amount": 3000.0, "date": "01.07.2018", "category": "Переводы", "description": "Петров В"}]


@pytest.fixture
def test_top_transactions_sort():
    """тестовый датафрейм"""
    data = {
        "last_digits": ["*1111", "*1111", "*2222", "*3333", "*3333"],
        "transaction_date": [
            "28.07.2018 15:00:00",
            "27.07.2018 15:00:00",
            "25.07.2018 15:00:00",
            "23.07.2018 15:00:00",
            "23.07.2018 15:00:00",
        ],
        "payment_amount": [-1000, -2000, -3000, -3000, 3000],
        "status": ["OK", "OK", "OK", "Failed", "OK"],
        "description": ["test1", "test1", "test1", "test1", "test1"],
        "category": ["Food", "Clothing", "Clothing", "Clothing", "Clothing"],
        "payment_date": ["28.07.2018", "27.07.2018", "25.07.2018", "23.07.2018", "23.07.2018"],
    }
    return pd.DataFrame(data, index=[0, 1, 2, 3, 4])


def test_top_transactions_new_df(test_top_transactions_sort):
    """тест сортировки и группировки файла"""
    result = top_transactions(test_top_transactions_sort, "29.07.2018")
    assert result == [
        {"amount": 3000.0, "date": "25.07.2018", "category": "Clothing", "description": "test1"},
        {"amount": 2000.0, "date": "27.07.2018", "category": "Clothing", "description": "test1"},
        {"amount": 1000.0, "date": "28.07.2018", "category": "Food", "description": "test1"},
    ]

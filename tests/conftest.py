import pandas as pd
import pytest


@pytest.fixture
def data_fame_test():
    diction = [
        {
            "transaction_date": "04.01.2018 15:00:41",
            "payment_date": "04.01.2018",
            "last_digits": "*1111",
            "status": "OK",
            "transaction_amount": -1005.0,
            "transaction_currency": "RUB",
            "payment_amount": -1025.0,
            "payment_currency": "RUB",
            "cashback": None,
            "category": "Топливо",
            "description": "Pskov AZS 12 K2",
            "bonuses": 20,
            "investment_box": 0,
            "rounding_amount": 1025.0,
        },
        {
            "transaction_date": "04.02.2018 14:05:08",
            "payment_date": "04.02.2018",
            "last_digits": "*1111",
            "status": "OK",
            "transaction_amount": -1065.9,
            "transaction_currency": "RUB",
            "payment_amount": -1065.9,
            "payment_currency": "RUB",
            "cashback": None,
            "category": "Супермаркеты",
            "description": "Пятёрочка",
            "bonuses": 21,
            "investment_box": 0,
            "rounding_amount": 1065.9,
        },
        {
            "transaction_date": "03.03.2018 15:03:35",
            "payment_date": "03.03.2018",
            "last_digits": "*1111",
            "status": "OK",
            "transaction_amount": -73.06,
            "transaction_currency": "RUB",
            "payment_amount": -73.06,
            "payment_currency": "RUB",
            "cashback": None,
            "category": "Супермаркеты",
            "description": "Magazin 25",
            "bonuses": 1,
            "investment_box": 0,
            "rounding_amount": 73.06,
        },
        {
            "transaction_date": "03.04.2018 14:55:21",
            "payment_date": "03.04.2018",
            "last_digits": "*7197",
            "status": "FAILED",
            "transaction_amount": -21.0,
            "transaction_currency": "RUB",
            "payment_amount": -21.0,
            "payment_currency": "RUB",
            "cashback": None,
            "category": "Красота",
            "description": "OOO Balid",
            "bonuses": 0,
            "investment_box": 0,
            "rounding_amount": 21.0,
        },
        {
            "transaction_date": "01.05.2018 20:27:51",
            "payment_date": "01.05.2018",
            "last_digits": "*7197",
            "status": "OK",
            "transaction_amount": -316.0,
            "transaction_currency": "RUB",
            "payment_amount": -316.0,
            "payment_currency": "RUB",
            "cashback": None,
            "category": "Красота",
            "description": "OOO Balid",
            "bonuses": 6,
            "investment_box": 0,
            "rounding_amount": 316.0,
        },
        {
            "transaction_date": "01.06.2018 12:49:53",
            "payment_date": "01.06.2018",
            "last_digits": "*2222",
            "status": "OK",
            "transaction_amount": -300.0,
            "transaction_currency": "RUB",
            "payment_amount": -3000.0,
            "payment_currency": "RUB",
            "cashback": None,
            "category": "Мобильная связь",
            "description": "Я МТС +7 999 11-22-33",
            "bonuses": 0,
            "investment_box": 0,
            "rounding_amount": 3000.0,
        },
        {
            "transaction_date": "01.07.2018 12:49:53",
            "payment_date": "01.07.2018",
            "last_digits": None,
            "status": "OK",
            "transaction_amount": 5000.0,
            "transaction_currency": "RUB",
            "payment_amount": -3000.0,
            "payment_currency": "RUB",
            "cashback": None,
            "category": "Переводы",
            "description": "Петров В",
            "bonuses": 0,
            "investment_box": 0,
            "rounding_amount": 3000.0,
        },
    ]
    return pd.DataFrame(diction, index=[0, 1, 2, 3, 4, 5, 6])


@pytest.fixture
def test_dict():
    return [
        {"description": "test_1", "category": "test_1"},
        {"description": "test_2", "category": "test_2"},
        {"description": "Петров С.", "category": "Переводы"},
        {"description": "МТС Mobile +7 921 999-99-99", "category": "test_1"},
        {"description": "Мегафон +7 921 999-99-99", "category": "Переводы"},
    ]


@pytest.fixture
def test_category_data():
    """тестовый датафрейм"""
    data = {
        "transaction_date": ["28.07.2018", "29.07.2018", "30.07.2018", "30.04.2018", "29.04.2018"],
        "category": ["Food", "Clothing", "Clothing", "Clothing", "Clothing"],
        "payment_amount": [-100, -200, 300, -400, -500],
        "status": ["FAILED", "OK", "OK", "OK", "OK"],
        "payment_date": ["28.07.2018", "29.07.2018", "30.07.2018", "30.04.2018", "29.04.2018"],
    }
    return pd.DataFrame(data, index=[0, 1, 2, 3, 4])

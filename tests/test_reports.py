import tempfile

import pandas as pd
from pandas._testing import assert_frame_equal

from src.reports import dataframe_to_json, save_to_file, spending_by_category


def test_spending_by_category_normal_df(data_fame_test):
    """тест копии реального файла"""
    result = spending_by_category(data_fame_test, "Мобильная связь", "28.07.2018")
    expected_output = pd.DataFrame(
        [
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
            }
        ],
        index=[5],
    )
    assert_frame_equal(result, expected_output)


def test_spending_by_category_new_df(test_category_data):
    """тест фильтрации условий, дата 3 месяца, категорииб отрицательная цена"""
    expected_output = pd.DataFrame(
        {
            "transaction_date": ["29.07.2018", "30.04.2018"],
            "category": ["Clothing", "Clothing"],
            "payment_amount": [-200, -400],
            "status": ["OK", "OK"],
            "payment_date": ["29.07.2018", "30.04.2018"],
        },
        index=[1, 3],
    )

    result = spending_by_category(test_category_data, "Clothing", "30.07.2018")
    assert_frame_equal(result, expected_output)


def test_save_to_file_txt():
    """Тестирует запись в файл .txt"""

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        txt_file_path = tmp_file.name

    @save_to_file(file_name=txt_file_path)
    def print_text(x):
        return x

    print_text("test_text")

    with open(f"{txt_file_path}.txt", "r", encoding="utf-8") as file:
        file_txt = file.read()

    assert file_txt == "test_text"


def test_save_to_file_csv():
    """Тестирует запись в файл .csv"""

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        csv_file_path = tmp_file.name

    @save_to_file(file_name=csv_file_path)
    def test_data_csv():
        data = {
            "transaction_date": ["28.07.2018", "29.07.2018"],
            "category": ["Food", "Clothing"],
            "payment_amount": [-10, -20],
        }
        return pd.DataFrame(data)

    test_data_csv()

    with open(f"{csv_file_path}.csv", "r", encoding="utf-8") as file:
        csv_file = file.read()

    assert csv_file == "28.07.2018     Food -10\n29.07.2018 Clothing -20"


def test_dataframe_to_json(test_category_data):
    result = dataframe_to_json(test_category_data)
    assert result == (
        "[\n"
        "    {\n"
        '        "transaction_date":"28.07.2018",\n'
        '        "category":"Food",\n'
        '        "payment_amount":-100,\n'
        '        "status":"FAILED",\n'
        '        "payment_date":"28.07.2018"\n'
        "    },\n"
        "    {\n"
        '        "transaction_date":"29.07.2018",\n'
        '        "category":"Clothing",\n'
        '        "payment_amount":-200,\n'
        '        "status":"OK",\n'
        '        "payment_date":"29.07.2018"\n'
        "    },\n"
        "    {\n"
        '        "transaction_date":"30.07.2018",\n'
        '        "category":"Clothing",\n'
        '        "payment_amount":300,\n'
        '        "status":"OK",\n'
        '        "payment_date":"30.07.2018"\n'
        "    },\n"
        "    {\n"
        '        "transaction_date":"30.04.2018",\n'
        '        "category":"Clothing",\n'
        '        "payment_amount":-400,\n'
        '        "status":"OK",\n'
        '        "payment_date":"30.04.2018"\n'
        "    },\n"
        "    {\n"
        '        "transaction_date":"29.04.2018",\n'
        '        "category":"Clothing",\n'
        '        "payment_amount":-500,\n'
        '        "status":"OK",\n'
        '        "payment_date":"29.04.2018"\n'
        "    }\n"
        "]"
    )

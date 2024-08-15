from unittest.mock import mock_open, patch

from src.services import people_search, phone_number_search, simple_search


@patch("builtins.open", new_callable=mock_open, read_data="data")
def test_simple_search_open(mock_file):
    assert open("../Data/transactions_excel.xlsx").read() == "data"
    mock_file.assert_called_with("../Data/transactions_excel.xlsx")


@patch("json.load")
def test_simple_search(mock_file, test_dict):
    mock_file.return_value = {"user_simple_search": "test_1"}
    result = simple_search(test_dict, "user_settings.json")
    assert result == (
        "[\n"
        "    {\n"
        '        "description": "test_1",\n'
        '        "category": "test_1"\n'
        "    },\n"
        "    {\n"
        '        "description": "МТС Mobile +7 921 999-99-99",\n'
        '        "category": "test_1"\n'
        "    }\n"
        "]"
    )


def test_phone_number_search(test_dict):
    result = phone_number_search(test_dict)
    assert result == (
        "[\n"
        "    {\n"
        '        "description": "МТС Mobile +7 921 999-99-99",\n'
        '        "category": "test_1"\n'
        "    },\n"
        "    {\n"
        '        "description": "Мегафон +7 921 999-99-99",\n'
        '        "category": "Переводы"\n'
        "    }\n"
        "]"
    )


def test_people_search(test_dict):
    result = people_search(test_dict)
    assert result == (
        "[\n" "    {\n" '        "description": "Петров С.",\n' '        "category": "Переводы"\n' "    }\n" "]"
    )

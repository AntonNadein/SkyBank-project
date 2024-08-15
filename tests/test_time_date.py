import datetime
from unittest.mock import mock_open, patch

import pytest
from freezegun import freeze_time

from src.time_data import date_first_day_months, date_per_quarter, datetime_to_time_date, greeting_by_time


@patch("builtins.open", new_callable=mock_open, read_data="data")
def test_datetime_to_time_date_open(mock_file):
    assert open("../Data/transactions_excel.xlsx").read() == "data"
    mock_file.assert_called_with("../Data/transactions_excel.xlsx")


@patch("json.load")
def test_datetime_to_time_date(mock_file):
    """Преобразование полученной даты"""
    mock_file.return_value = {"user_date": ["2022-12-31 11:20:16"]}
    result = datetime_to_time_date("user_settings.json")
    assert result == ("31.12.2022", "11:20")


@freeze_time("2012-01-14")
@patch("json.load")
def test_datetime_to_time_date_now(mock_file):
    """Преобразование текущей даты"""
    mock_file.return_value = {"user_date": None}
    result = datetime_to_time_date("user_settings.json")
    assert result == ("14.01.2012", "00:00")


@pytest.mark.parametrize(
    "times, expected",
    [
        ("12:00", "Добрый день"),
        ("18:00", "Добрый вечер"),
        ("21:59", "Добрый вечер"),
        ("22:00", "Доброй ночи"),
        ("23:59", "Доброй ночи"),
        ("00:00", "Доброй ночи"),
        ("05:59", "Доброй ночи"),
        ("06:00", "Доброе утро"),
    ],
)
def test_greeting_by_time(times, expected):
    """Тест приветствия"""
    assert (greeting_by_time(times)) == expected


@freeze_time("2012-01-14 06:00")
def test_greeting_by_time_now():
    """Тест приветствия текущего времени"""
    assert (greeting_by_time()) == "Доброе утро"


def test_date_first_day_months():
    """Тест времени до первого числа"""
    result = date_first_day_months("01.07.2014")
    result_last_day = date_first_day_months("31.07.2014")
    assert result == (datetime.datetime(2014, 7, 1, 0, 0), datetime.datetime(2014, 7, 1, 0, 0))
    assert result_last_day == (datetime.datetime(2014, 7, 31, 0, 0), datetime.datetime(2014, 7, 1, 0, 0))


@freeze_time("2024-01-14")
def test_date_first_day_months_now():
    """Тест времени до первого числа от текущей даты"""
    result = date_first_day_months()
    assert result == (datetime.datetime(2024, 1, 14, 0, 0), datetime.datetime(2024, 1, 1, 0, 0))


def test_date_per_quarter():
    """Тест времени минус квартал"""
    result = date_per_quarter("01.07.2014")
    result_last_day = date_per_quarter("31.07.2014")
    assert result == (datetime.datetime(2014, 7, 1, 0, 0), datetime.datetime(2014, 4, 1, 0, 0))
    assert result_last_day == (datetime.datetime(2014, 7, 31, 0, 0), datetime.datetime(2014, 4, 30, 0, 0))


@freeze_time("2024-01-14")
def test_date_per_quarter_now():
    """Тест времени минус квартал от текущей даты"""
    result = date_first_day_months()
    assert result == (datetime.datetime(2024, 1, 14, 0, 0), datetime.datetime(2024, 1, 1, 0, 0))

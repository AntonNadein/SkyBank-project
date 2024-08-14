import logging
import os
from functools import wraps
from typing import Any, Callable

import pandas as pd
from pandas import DataFrame

from src.constant import PATH_TO_FILE
from src.logger import setup_logging_services_reports
from src.time_data import date_per_quarter
from src.utils import open_excel

setup_logging_services_reports()
spending_by_category_logger = logging.getLogger("app.home_page")


def save_to_file(file_name: str = "report") -> Callable:
    """Декоратор сохранения в файл"""

    def my_decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            if type(result) is DataFrame:
                file_names = f"{file_name}.csv"
                with open(os.path.join(PATH_TO_FILE, file_names), "w", encoding="utf-8") as file:
                    file.write(result.to_string(header=False, index=False))
            else:
                file_names = f"{file_name}.txt"
                with open(os.path.join(PATH_TO_FILE, file_names), "w", encoding="utf-8") as file:
                    file.write(result)

        return wrapper

    return my_decorator


# @save_to_file('examp')
def spending_by_category(transactions: pd.DataFrame, category: str, date: str) -> pd.DataFrame:
    """Фильтр трат по категории"""
    date_end, date_start = date_per_quarter(date)
    spending_by_category_logger.info(f"Категория поиска: {category}")
    spending_by_category_logger.info(f"Даты поиска: Начало: {date_start} Конец: {date_end}")
    # Фильтр дата за 3 месяца, категория, траты
    transactions_by_category_date = transactions.loc[
        (pd.to_datetime(transactions.transaction_date, dayfirst=True) <= date_end)
        & (pd.to_datetime(transactions.transaction_date, dayfirst=True) >= date_start)
        & (transactions.category == category)
        & (transactions.payment_amount < 0)
    ]
    return transactions_by_category_date


# file_open = open_excel("operations.xlsx")
#
# end_df = spending_by_category(file_open,"Пополнения", "30.03.2020")
# # print(type(end_df)) <class 'pandas.core.frame.DataFrame'>Супермаркеты  & (transactions.payment_amount < 0)
# print((end_df).shape)
# print((end_df).head())
# print(end_df)

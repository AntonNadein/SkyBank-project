import json
import logging

from src.logger import setup_logging
from src.time_data import datetime_to_time_date, greeting_by_time
from src.utils import card_info, open_excel, request_tickers, top_transactions, user_stocks_moex

setup_logging()
home_page_logger = logging.getLogger("app.home_page")


def home_page():
    """Функционал «Главной» страницы"""
    json_answer = {}
    data_frame_file = "operations.xlsx"
    request_file = "user_settings.json"
    home_page_logger.info(f"Открыт файл {data_frame_file} \n" f"Открыт файл {request_file}")
    dates, times = datetime_to_time_date(request_file)
    data_frame = open_excel(data_frame_file)

    greeting = greeting_by_time(times)
    json_answer["greeting"] = greeting
    home_page_logger.info(f"Результат работы greeting_by_time {greeting}")

    cards = card_info(data_frame, dates)
    json_answer["cards"] = cards
    home_page_logger.info(f"Результат работы card_info {cards}")

    top_transaction = top_transactions(data_frame, dates)
    json_answer["top_transactions"] = top_transaction
    home_page_logger.info(f"Результат работы top_transactions {top_transaction}")

    currency_rates = request_tickers(request_file)
    json_answer["currency_rates"] = currency_rates
    home_page_logger.info(f"Результат работы currency_rates {currency_rates}")

    stock_prices = user_stocks_moex(request_file)
    json_answer["stock_prices"] = stock_prices
    home_page_logger.info(f"Результат работы user_stocks_moex {stock_prices}")

    json_data = json.dumps(json_answer, ensure_ascii=False, indent=4)
    return json_data


print(home_page())

import requests
import json
from config import money


class ConvertationException(Exception):
    pass


class MoneyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertationException(f'Невозможно валюту {quote} перевести в саму себя.')

        try:
            quote_ticker = money[quote]
        except KeyError:
            raise ConvertationException(f'Не удалось обработать неизвестную валюту - {quote}. \
        \nОтправьте /values, чтобы посмотреть список доступных валют.')

        try:
            base_ticker = money[base]
        except KeyError:
            raise ConvertationException(f'Не удалось обработать неизвестную валюту - {base}. \
        \nОтправьте /values, чтобы посмотреть список доступных валют.')

        try:
            amount = float(amount)
            if float(amount) > 0:
                amount = float(amount)
            else:
                raise ConvertationException(f'Количество не может быть отрицательным: {amount}.')
        except ValueError:
            raise ConvertationException(f'Введено несуществующее количество: {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[money[base]]

        return round(float(total_base * amount), 2)

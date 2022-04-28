import requests
import json
from values import keys

class APIException (Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base:str,quote:str,amount:str):
    # если узнаем цену определенного валюты в ней же, количество будет тем же самым
        if quote == base:
            total_base=amount
        else:
            try:
                base_ticker = keys[base]
            except KeyError:
                raise APIException(f'Неверно введено наименование валюты "{base}"')

            try:
                quote_ticker = keys[quote]
            except KeyError:
                raise APIException(f'Неверно введено наименование валюты "{quote}"')
            try:
                amount = float(amount)
            except ValueError:
                raise APIException('Количество переводимой валюты должно быть числом')

            r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
            total_base = round((json.loads(r.content)[keys[quote]])*amount, 3)


        return total_base
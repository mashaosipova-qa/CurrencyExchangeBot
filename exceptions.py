import requests
import json
from config import keys

class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        # base - валюта, которую конвертируем
        # quote - валюта, в которую конвертируем
        # amount - количество


        if quote.lower() not in keys:
            raise APIException(f'Валюта "{quote}" не найдена. Посмотрите список: /values')
        if base.lower() not in keys:
            raise APIException(f'Валюта "{base}" не найдена. Посмотрите список: /values')
        if quote.lower() == base.lower():
            raise APIException(f'Введите различные валюты')

        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')
        if amount <= 0:
            raise APIException(f'Количество должно быть больше нуля')

        try:
            response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{base_ticker}')
            data = json.loads(response.content)

            if 'rates' not in data:
                raise APIException(f'Не удалось получить курсы валют')

            if quote_ticker not in data['rates']:
                raise APIException(f'Не удалось получить курс для пары {base}/{quote}')

            rate = data['rates'][quote_ticker] # курс конвертации из API (сколько стоит 1 единица base валюты в quote валюте)

            total = rate * amount
            total = round(total, 2)

            return total

        except Exception as e:
            raise APIException(f'Ошибка при обращении к API: {e}')




import telebot

from config import TOKEN, keys
from exceptions import APIException, CryptoConverter

CurrencyBot = telebot.TeleBot(TOKEN)

@CurrencyBot.message_handler(commands=['start', 'helpMe'])
def helpMe(message: telebot.types.Message):
    text = 'Для начала работы введите команду в следующем формате (через пробел):\n' \
           '• Название валюты, которую конвертируете\n' \
           '• Название валюты, в которую конвертируете\n' \
           '• Количество первой валюты\n\n' \
           'Пример: евро доллар 100\n\n' \
           'Список доступных валют: /values'

    CurrencyBot.reply_to(message, text)


@CurrencyBot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    CurrencyBot.reply_to(message, text)


# base, quote, amount = message.text.split(' ')
@CurrencyBot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    if message.text.startswith('/'):
        return
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверно введены параметры.')

        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        CurrencyBot.reply_to(message, f'Ошибка пользователя. \n{e}')

    except Exception as e:
        CurrencyBot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        rate = total_base / float(amount)
        text = f' {amount} {base} = {total_base} {quote}\n Курс: 1 {base} = {round(rate, 4)} {quote}'
        CurrencyBot.send_message(message.chat.id, text)


CurrencyBot.polling(none_stop=True)


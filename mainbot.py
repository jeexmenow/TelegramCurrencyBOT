import telebot
from set import keys, TOKEN
from exceptions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

#старт и пояснение для ввода
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет! ☺️ Для начала работы введите команду в следующем виде: \n<имя валюты (ед.ч)> \
<валюта для перевода(ед.ч)> \
<количество переводимой валюты>\nТакже вы можете увидеть список всех доступных валют 😉: /values'
    bot.reply_to(message, text)

#список доступных валют
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

#ответы при ошибке ввода
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров 😕')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя 😕\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду 😔\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
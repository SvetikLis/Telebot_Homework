import telebot
from config import keys, TOKEN
from extensions import CryptoConverter, ConversionException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def repeat(message: types.Message):
   text = 'Для начала работы с ботом, введите команду в следующем формате: \n<наименование валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n Посмотреть список всех доступных валют: /values'
   bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
       text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise ConversionException('Слишком много параметров.')

        if len(values) < 3:
            raise ConversionException('Слишком мало параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        raise bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
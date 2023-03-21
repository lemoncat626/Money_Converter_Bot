import telebot
from config import money, TOKEN
from extensions import ConvertationException, MoneyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def help(message: telebot.types.Message):
    text = f'Приветствую, {message.chat.username}! \nЭто бот-конвертер валюты. \
\nЧтобы узнать как он работает, вызовите команду /help.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы произвести конвертацию валют, введите команду в следующем формате: \
\n<имя переводимой валюты> \
<в какую валюту перевести> \
<количество> \nПосмотреть список доступных валют для конвертации: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Список доступных для конвертации валют:'
    for key in money.keys():
        text = '\n'.join((text, key.capitalize()))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise ConvertationException('Неверное количество элементов ввода.')

        quote, base, amount = values
        total_base = MoneyConverter.get_price(quote, base, amount)
    except ConvertationException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Стоимость {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()

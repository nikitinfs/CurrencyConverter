import telebot
import config
import exc

bot = telebot.TeleBot(config.token)

parametrs = ['', '', '']

language_id = 0


@bot.message_handler(commands=['start'])
def start_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Rus', callback_data='ru'))
    keyboard.row(
        telebot.types.InlineKeyboardButton('Eng', callback_data='en')
    )
    bot.send_message(
        message.chat.id,
        'Привет! Выбери язык:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global language_id
    if call.message:
        if call.data == 'ru':
            language_id = 1
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('1. Узнать текущий курс валют', callback_data='meth1'))
            keyboard.row(
                telebot.types.InlineKeyboardButton('2. Перевести деньги в другую валюту', callback_data='meth2')                )
            bot.send_message(call.message.chat.id,'Выберите действие:', reply_markup=keyboard)
        elif call.data == 'en':
            language_id = 2
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('1. Find out current exchange rate', callback_data='meth1'))
            keyboard.row(
                telebot.types.InlineKeyboardButton('2. Transfer money to another currency', callback_data='meth2'))
            bot.send_message(call.message.chat.id, 'Select an action:', reply_markup=keyboard)
        elif call.data == 'meth1':
            message = ''
            if language_id == 1:
                message = "Выберите валюту: "
            elif language_id == 2:
                message = "Choose currency: "
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                    telebot.types.InlineKeyboardButton('USD', callback_data='usd'),
                    telebot.types.InlineKeyboardButton('EUR', callback_data='eur'),
                    telebot.types.InlineKeyboardButton('GBP', callback_data='gbp'))
            bot.send_message(call.message.chat.id, message, reply_markup=keyboard)
        elif call.data == 'usd':
            bot.send_message(call.message.chat.id, 'Курс доллара: ' + str(exc.kurs(config.USD)))
        elif call.data == 'eur':
            bot.send_message(call.message.chat.id, 'Курс евро: ' + str(exc.kurs(config.EUR)))
        elif call.data == 'gbp':
            bot.send_message(call.message.chat.id, 'Курс фунта: ' + str(exc.kurs(config.GBP)))
        elif call.data == 'meth2':
            message = ''
            if language_id == 1:
                message = "Выберите валюту для обмена: "
            elif language_id == 2:
                message = "Select currency to exchange: "
            bot.send_message(call.message.chat.id, message, reply_markup=exc.keyb1)


@bot.message_handler(commands=['exchange'])
def meth_exchange(message):
    bot.send_message(message.chat.id, 'Выберите валюту для обмена:', reply_markup=exc.keyb1)

@bot.message_handler(content_types=['text'])
def get_name(message):
    parametrs[0] = message.text
    bot.send_message(message.chat.id, 'Напишите сумму для обмена' )
    bot.register_next_step_handler(message, get_quantity)

def get_quantity(message):
    parametrs[1] = message.text
    bot.send_message(message.chat.id, 'Выберите желаемую валюту',  reply_markup=exc.keyb1)
    bot.register_next_step_handler(message, get_name2)

def get_name2(message):
    parametrs[2] = message.text
    k = exc.exchange(parametrs[0], float(parametrs[1]), parametrs[2])
    bot.send_message(message.chat.id, parametrs[1] + ' ' + parametrs[0] + ' = ' + str(k) + ' ' + parametrs[2])
    print(parametrs)




bot.polling(none_stop=True)

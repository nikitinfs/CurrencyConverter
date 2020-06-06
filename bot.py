import telebot
import config
import exc

bot = telebot.TeleBot(config.token)

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

bot.polling(none_stop=True)

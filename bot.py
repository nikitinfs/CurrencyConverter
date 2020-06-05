import telebot
import config


bot = telebot.TeleBot(config.token)


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
    if call.message:
        if call.data == 'ru':
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('1. Узнать текущий курс валют.', callback_data='ru'))
            keyboard.row(
                telebot.types.InlineKeyboardButton('2. Узнать сколько денег в другой валюте.', callback_data='en')                )
            bot.send_message(call.message.chat.id,'Выберите действие:', reply_markup=keyboard)
        elif call.data == 'en':
            bot.send_message(call.message.chat.id, 'Next time')

bot.polling(none_stop=True)

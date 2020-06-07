import telebot
import config
import exc
import datetime

bot = telebot.TeleBot(config.token)

parametrs = ['', '', '']

language_id = 0
currency_id = ''
currency_name = ''


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

@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    message_lan = ''
    if language_id == 1:
        message_lan = "Написать разработчику"
    elif language_id == 2:
        message_lan = "Message the developer"
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            message_lan, url='telegram.me/babessssssss'
        )
    )
    if language_id == 1:
        bot.send_message(
        message.chat.id,
        '1) Для обмена валюты нажмите /exchange.\n' +
        '2) Нажмите на интересующую вас валюту.\n' +
        '3) Вы получите сообщение, содержащее информацию о валюте.\n' +
        '4) Нажмите "обновить",чтобы получить информацию относительно запроса.\n' +
        '5) Бот поддерживает режим инлайн. Наберите @currencyex_bot в любом чате.',
        reply_markup=keyboard )
    elif language_id == 2:
        bot.send_message(
            message.chat.id,
            '1) To exchange currency press /exchange.\n' +
            '2) Click on the currency you are interested in.\n' +
            '3) You will receive a message containing information regarding the currency. \n' +
            '4) Click “Update” to receive the current information regarding the request. \n' +
            '5) The bot supports inline. Type @currencyex_bot in any chat.',
            reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global language_id
    global currency_id
    global currency_name
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

        elif call.data == 'update':
            k = exc.kurs(currency_id)
            messagem4 = ['', '', '', '']
            if language_id == 1:
                messagem4[0] = "Курс "
                messagem4[1] = 'Поделиться'
                messagem4[2] = "Обновить"
                messagem4[3] = 'Обновлено: '
            elif language_id == 2:
                messagem4[0] = "Rate "
                messagem4[1] = 'Share'
                messagem4[2] = "Update"
                messagem4[3] = 'Updated: '
            answer = messagem4[0] + currency_name + ': ' + str(k)
            timenow = datetime.datetime.now()
            timenow = str(timenow)
            timenow = timenow[:16]
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton(messagem4[1], switch_inline_query=answer),
                telebot.types.InlineKeyboardButton(messagem4[2], callback_data='update'))
            bot.send_message(call.message.chat.id, answer + "\n"
                             + messagem4[3] + timenow, reply_markup=keyboard)
        elif call.data == 'usd':
            messagem = ['', '', '']
            if language_id == 1:
                messagem[0] = 'Курс доллара: '
                messagem[1] = 'Поделиться'
                messagem[2] = 'Обновить'
            elif language_id == 2:
                messagem[0] = 'Dollar rate: '
                messagem[1] = 'Share'
                messagem[2] = 'Update'
            k = exc.kurs(config.USD)
            answer = messagem[0] + str(k)
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton(messagem[1], switch_inline_query=answer),
                telebot.types.InlineKeyboardButton(messagem[2], callback_data='update'))
            bot.send_message(call.message.chat.id, answer, reply_markup=keyboard)
            currency_id = config.USD
            if language_id == 1:
                currency_name = "доллар"
            elif language_id == 2:
                currency_name = 'dollar'
        elif call.data == 'eur':
            messagem = ['', '', '']
            if language_id == 1:
                messagem[0] = 'Курс евро: '
                messagem[1] = 'Поделиться'
                messagem[2] = 'Обновить'
            elif language_id == 2:
                messagem[0] = 'Euro rate: '
                messagem[1] = 'Share'
                messagem[2] = 'Update'
            k = exc.kurs(config.EUR)
            answer = messagem[0] + str(k)
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton(messagem[1], switch_inline_query=answer),
                telebot.types.InlineKeyboardButton(messagem[2], callback_data='update'))
            bot.send_message(call.message.chat.id, answer, reply_markup=keyboard)
            currency_id = config.EUR
            if language_id == 1:
                currency_name = "евро"
            elif language_id == 2:
                currency_name = 'euro'
        elif call.data == 'gbp':
            messagem = ['', '', '']
            if language_id == 1:
                messagem[0] = 'Курс фунта: '
                messagem[1] = 'Поделиться'
                messagem[2] = 'Обновить'
            elif language_id == 2:
                messagem[0] = 'Pound rate: '
                messagem[1] = 'Share'
                messagem[2] = 'Update'
            answer = 'Курс фунта: ' + str(exc.kurs(config.GBP))
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton(messagem[1], switch_inline_query=answer),
                telebot.types.InlineKeyboardButton(messagem[2], callback_data='update'))
            bot.send_message(call.message.chat.id, answer, reply_markup=keyboard)
            currency_id = config.GBP
            if language_id == 1:
                currency_name = "фунта"
            elif language_id == 2:
                currency_name = 'GBP'
        elif call.data == 'meth2':
            message = ''
            if language_id == 1:
                message = "Выберите валюту для обмена: "
            elif language_id == 2:
                message = "Select currency to exchange: "
            bot.send_message(call.message.chat.id, message, reply_markup=exc.keyb1)



@bot.message_handler(commands=['exchange'])
def meth_exchange(message):
    message_lan = ''
    if language_id == 1:
        message_lan = "Выберите валюту для обмена"
    elif language_id == 2:
        message_lan = "Select currency to exchange"
    bot.send_message(message.chat.id, message_lan, reply_markup=exc.keyb1)

@bot.message_handler(content_types=['text'])
def get_name(message):
    message_lan =''
    if language_id == 1:
        message_lan = "Напишите сумму для обмена"
    elif language_id == 2:
        message_lan = 'Type the amount for exchange'
    parametrs[0] = message.text
    bot.send_message(message.chat.id, message_lan)
    bot.register_next_step_handler(message, get_quantity)

def get_quantity(message):
    message_lan = ''
    if language_id == 1:
        message_lan = "Выберите желаемую валюту"
    elif language_id == 2:
        message_lan = 'Choose preferred currency'
    parametrs[1] = message.text
    bot.send_message(message.chat.id, message_lan,  reply_markup=exc.keyb1)
    bot.register_next_step_handler(message, get_name2)

def get_name2(message):
    parametrs[2] = message.text
    k = exc.exchange(parametrs[0], float(parametrs[1]), parametrs[2])
    bot.send_message(message.chat.id, parametrs[1] + ' ' + parametrs[0] + ' = ' + str(k) + ' ' + parametrs[2])
    print(parametrs)

@bot.inline_handler(func=lambda query: True)
def query_text(inline_query):
    res = exc.Curses()
    bot.answer_inline_query(
        inline_query.id,
        get_iq_articles(res)
    )


def get_iq_articles(exchanges):
    result = []
    names = ["USD", "EUR", "GBP"]
    k = 0
    messagem = ['', '', '']
    if language_id == 1:
        messagem[0] = 'Перейти в бот'
        messagem[1] = 'Курс '
        messagem[2] = 'Обменять RUB'
    if language_id == 1:
        messagem[0] = 'Go to bot'
        messagem[1] = 'Rate  '
        messagem[2] = 'Convert RUB'

    for i in exchanges:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(telebot.types.InlineKeyboardButton(messagem[0], url=config.url))
        result.append(
            telebot.types.InlineQueryResultArticle(id=k, title=names[k],
	        input_message_content=telebot.types.InputTextMessageContent(messagem[1] + names[k] + ": " + str(exchanges[k])),
            reply_markup=keyboard, description = messagem[2] + ' -> ' + names[k]))
        k = k + 1
    return result


bot.polling(none_stop=True)


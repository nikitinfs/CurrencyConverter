import requests
import config
import xmltodict
import telebot


keyb1 = telebot.types.ReplyKeyboardMarkup()
button_RUB = telebot.types.KeyboardButton('RUB')
button_USD = telebot.types.KeyboardButton('USD')
button_EUR = telebot.types.KeyboardButton('EUR')
button_GBP = telebot.types.KeyboardButton('GBP')
keyb1.add(button_RUB, button_USD, button_EUR, button_GBP)

def kurs(name_valute):
    r = requests.get(config.URL)
    resp = r.text
    data = xmltodict.parse(resp)


    for i in data['ValCurs']['Valute']:
        if i['@ID'] == name_valute:
            Curs_Valute = i['Value']
            break
    Curs_Valute = Curs_Valute[:2] +'.'+Curs_Valute[3:]
    Curs_Valute = float(Curs_Valute)
    return Curs_Valute

def exchange(name_1, quantity_1, name_2):
    quantity_2 = 0
    if name_1 == "RUB" and name_2 == "USD":
        k = kurs(config.USD)
        quantity_2 = quantity_1/k
    elif name_1 == "RUB" and name_2 == "EUR":
        k = kurs(config.EUR)
        quantity_2 = quantity_1/k
    elif name_1 == "RUB" and name_2 == "GBP":
        k = kurs(config.GBP)
        quantity_2 = quantity_1/k
    elif name_1 == "USD" and name_2 == "RUB":
        k = kurs(config.USD)
        quantity_2 = quantity_1 * k
    elif name_1 == "USD" and name_2 == "EUR":
        k = kurs(config.EUR)
        k1 = kurs(config.USD)
        quantity_2 = k1 * quantity_1/k
    elif name_1 == "USD" and name_2 == "GBP":
        k = kurs(config.GBP)
        k1 = kurs(config.USD)
        quantity_2 = quantity_1 * k1 / k
    elif name_1 == "EUR" and name_2 == "RUB":
        k = kurs(config.EUR)
        quantity_2 = quantity_1 * k
    elif name_1 == "EUR" and name_2 == "USD":
        k = kurs(config.USD)
        k1 = kurs(config.EUR)
        quantity_2 = k1 * quantity_1/k
    elif name_1 == "EUR" and name_2 == "GBP":
        k = kurs(config.GBP)
        k1 = kurs(config.EUR)
        quantity_2 = quantity_1 * k1 / k
    elif name_1 == "GBP" and name_2 == "RUB":
        k = kurs(config.GBP)
        quantity_2 = quantity_1 * k
    elif name_1 == "GBP" and name_2 == "EUR":
        k = kurs(config.EUR)
        k1 = kurs(config.GBP)
        quantity_2 = k1 * quantity_1/k
    elif name_1 == "GBP" and name_2 == "USD":
        k = kurs(config.USD)
        k1 = kurs(config.GBP)
        quantity_2 = quantity_1 * k1 / k

    return quantity_2

from telebot.types import ReplyKeyboardMarkup
from telebot.types import KeyboardButton


def welcome_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = KeyboardButton('Auto Ria')
    btn2 = KeyboardButton('Dou')

    markup.add(btn1, btn2)
    return markup


def auto_ria_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = KeyboardButton('Tesla')
    btn2 = KeyboardButton('Bmw')
    btn3 = KeyboardButton('Audi')
    btn4 = KeyboardButton('Citroen')
    btn5 = KeyboardButton('Volkswagen')
    btn6 = KeyboardButton('Chevrolet')
    btn7 = KeyboardButton('Opel')
    btn8 = KeyboardButton('Lamborghini')

    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    return markup


def dou_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = KeyboardButton('Python, junior')
    btn2 = KeyboardButton('Java, junior')
    btn3 = KeyboardButton('Php, junior')

    markup.add(btn1, btn2, btn3)
    return markup

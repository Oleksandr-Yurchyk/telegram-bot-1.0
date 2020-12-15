import telebot
from telebot.types import Message

from config import TOKEN
from keyboards import welcome_markup
from keyboards import auto_ria_markup
from keyboards import dou_markup
from common import search_car_by_parameter
from common import search_vacancy_by_parameter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message: Message):
    markup = welcome_markup()
    bot.send_message(message.chat.id,
                     f'Welcome {message.from_user.first_name} to the <b>{bot.get_me().first_name}</b> bot\n'
                     'Choose site you want to parse', parse_mode='html', reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == 'Auto Ria')
def auto_ria_search(message: Message):
    markup = auto_ria_markup()
    sent = bot.send_message(message.chat.id,
                            text='Choose one of the following car brand\n'
                                 'Or enter your own:',
                            reply_markup=markup)
    bot.register_next_step_handler(sent, car_brand)


def car_brand(message):
    markup = welcome_markup()
    bot.send_message(message.chat.id, text=f'Start parsing on auto-ria by parameter: {message.text}',
                     reply_markup=markup)
    search_car_by_parameter(bot, message)


@bot.message_handler(func=lambda m: m.text == 'Dou')
def dou_search(message: Message):
    markup = dou_markup()
    sent = bot.send_message(message.chat.id, text='Choose one of the following button\n'
                                                  'Or enter your own search', reply_markup=markup)
    bot.register_next_step_handler(sent, vacancy)


def vacancy(message):
    markup = welcome_markup()
    bot.send_message(message.chat.id, text=f'Start parsing on dou by parameter: {message.text}', reply_markup=markup)

    search_vacancy_by_parameter(bot, message)


if __name__ == '__main__':
    bot.polling(True)

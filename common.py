import time

from parsers import dou_parser
from parsers import auto_ria_parser


def search_vacancy_by_parameter(bot, message):
    category, search = message.text.split(',')
    vacancies = dou_parser.parse(category, search)
    for vacancy in vacancies:
        title = vacancy.get('title')
        link = vacancy.get('link')
        salary = vacancy.get('salary')
        if salary is None:
            salary = 'не вказано'

        bot.send_message(message.chat.id, f'{title},\nЗарплата: {salary},\n{link}')
    bot.send_message(message.chat.id, f'{len(vacancies)} vacancies found')


def search_car_by_parameter(bot, message):
    t1 = time.time()

    available_car_to_search = auto_ria_parser.get_all_brand_names()
    if message.text.lower() not in available_car_to_search:
        bot.send_message(message.chat.id, text='Sorry there are no car with that brand name\n'
                                               'Please enter valid brand name')
    else:
        count = 0
        cars = auto_ria_parser.threaded_parser(message.text)
        print(f'{(time.time() - t1)} sec')
        for car in cars:
            title = car.get('title')
            if message.text.lower() in title.lower():
                city = car.get('city')
                price = car.get('price')
                link = car.get('link')
                bot.send_message(message.chat.id, f'{title},\n{city},\n{price},\n{link}')
                count += 1
        bot.send_message(message.chat.id, f'{count} cars found')

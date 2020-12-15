from parsers import dou_parser
from parsers import auto_ria_parser
from config import logger


def search_vacancy_by_parameter(bot, message):
    try:
        logger.info(f'Searching vacancy with parameters - {message.text}')
        category, search = message.text.split(',')
    except ValueError:
        bot.send_message(message.chat.id, 'Wrong parameter! I expect two comma separated values\n'
                                          'programming language, vacancy description')
    else:
        vacancies = dou_parser.parse(category, search)
        for vacancy in vacancies:
            title = vacancy.get('title')
            link = vacancy.get('link')
            salary = vacancy.get('salary')
            if salary is None:
                salary = 'не вказано'

            bot.send_message(message.chat.id, f'{title},\nЗарплата: {salary},\n{link}')

        logger.info(f'{len(vacancies)} vacancies found')
        bot.send_message(message.chat.id, f'{len(vacancies)} vacancies found')


def search_car_by_parameter(bot, message):
    logger.info(f'Searching car with parameters - {message.text}')
    available_car_to_search = auto_ria_parser.get_all_brand_names()
    if message.text.lower() not in available_car_to_search:
        bot.send_message(message.chat.id, text='Sorry there are no car with that brand name\n'
                                               'Please enter valid brand name')
    else:
        count = 0
        cars = auto_ria_parser.threaded_parser(message.text)
        for car in cars:
            title = car.get('title')
            if message.text.lower() in title.lower():  # Condition 'if' for pages where less than 4 advertisements
                city = car.get('city')
                price = car.get('price')
                link = car.get('link')

                bot.send_message(message.chat.id, f'{title},\n{city},\n{price},\n{link}')
                count += 1

        logger.info(f'{count} cars found')
        bot.send_message(message.chat.id, f'{count} cars found')

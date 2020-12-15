import requests
from bs4 import BeautifulSoup
from config import logger

URL = f'https://jobs.dou.ua/vacancies'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'accept': '*/*'}


def get_html(params=None):
    return requests.get(URL, headers=HEADERS, params=params)


def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('li.l-vacancy')
    vacancies = []
    for item in items:
        if item.select_one('span.salary'):
            salary = item.select_one('div.title span').string.replace('\xa0', ' ')
        else:
            salary = None

        title = item.select_one('a.vt')
        vacancies.append({
            'title': title.string.replace('\xa0', ' '),
            'link': title.get('href'),
            'salary': salary,
        })
    return vacancies


def parse(category, search):
    html = get_html(params={'category': category, 'search': search, 'descr': 1})
    logger.info(f'Status code for this request - {html.status_code}')
    if html.status_code == 200:
        vacancies = []
        vacancies.extend(get_content(html.text))
        return vacancies
    else:
        logger.info('Something went wrong...')

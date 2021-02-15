import concurrent.futures
import requests
from bs4 import BeautifulSoup

from config import logger

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (HTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'accept': '*/*'}


def get_html(url, params=None):
    return requests.get(url, headers=HEADERS, params=params, )


def get_pages_count(html):
    soup = BeautifulSoup(html, 'lxml')
    pagination = soup.select('span.page-item.mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_all_brand_names():
    html = get_html('https://auto.ria.com/uk/newauto/catalog')
    soup = BeautifulSoup(html.text, 'lxml')

    all_brands = soup.select('span.name')
    brands = []
    for brand in all_brands:
        if brand.text not in brands:
            brands.append(brand.text.lower())
    return brands


def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('div.proposition')
    cars = []
    url = 'https://auto.ria.com'
    for item in items:
        cars.append({
            'title': item.select_one('h3.proposition_name').string.strip(),
            'link': f"{url}{item.select_one('div.proposition .proposition_link').get('href')}",
            'price': item.select_one('span.green.bold.size18').string.strip(),
            'city': item.select_one('div.proposition_region.size13 strong').string.strip(),
        })
    return cars


def threaded_parser(brand):
    """ Threaded parser to parse car data from auto.ria.com"""
    page = 1
    url = f'https://auto.ria.com/uk/newauto/marka-{brand}/?page={page}'
    html = get_html(url)
    get_all_brand_names()
    logger.info(f'Status code for this request - {html.status_code}')
    if html.status_code == 200:
        cars = []
        urls = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            logger.info(f'Parsing {brand}, {page} page of {pages_count}')
            urls.append(f'https://auto.ria.com/uk/newauto/marka-{brand}/?page={page}')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(get_html, url) for url in urls]
            for f in concurrent.futures.as_completed(results):
                cars.extend(get_content(f.result().text))
        return sorted(cars, key=lambda x: x['price'], reverse=True)
    else:
        logger.info('Something went wrong...')


def sync_parse(brand):
    """ Synchronous parser to parse car data from auto.ria.com"""
    url = f'https://auto.ria.com/uk/newauto/marka-{brand}/'
    html = get_html(url)
    get_all_brand_names()
    logger.info(f'Status code for this request - {html.status_code}')
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            logger.info(f'Parsing {brand}, {page} page of {pages_count}')
            html = get_html(url, params={'page': page})
            cars.extend(get_content(html.text))
        return sorted(cars, key=lambda x: x['price'], reverse=True)
    else:
        logger.info('Something went wrong...')

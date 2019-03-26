import json
import warnings
import urllib.request
from bs4 import BeautifulSoup

warnings.filterwarnings('ignore')

BASE_URL = 'https://ru.wowhead.com/'


def get_html(url):
    """Функция принимает URL, возвращает html этой страницы"""
    response = urllib.request.urlopen(url)
    return response.read()


def get_page_count(html):
    soup = BeautifulSoup(html)
    paggination = soup.find('table', class_='nav-pagination nav-pagination-position-bottom')
    return int(paggination.findAll('a')[-3].text)


def parse(html):
    """Функция обрабатывает html, достаёт нужные данные"""
    soup = BeautifulSoup(html)
    table = soup.findAll('div', class_='news-post news-post-style-teaser')

    news = []

    for i in range(len(table)):
        url = 'https://ru.wowhead.com/news={}'.format(table[i]['id'][10:])
        news.append({
            'url': url,
            'title': table[i].h1.a.text
        })

    return news


def save_news(news, path):
    with open(path + 'news.json', 'w') as file:
        json.dump(news, file, indent=5, ensure_ascii=True)


def main():
    """Функция запускает парсер"""
    page_count = get_page_count(get_html(BASE_URL))
    print('Всего найдено {} страниц'.format(page_count))

    news = []

    for page in range(1, page_count):
        print('Парсинг %d%%' % (page / page_count * 100))
        news.extend(parse(get_html(BASE_URL + 'news&p={}'.format(page))))

    save_news(news, 'parsed/')


if __name__ == '__main__':
    main()

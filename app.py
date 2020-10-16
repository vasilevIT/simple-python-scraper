"""
  Created by PyCharm.
  User: antonvasilev <bysslaev@gmail.com>
  Date: 16/10/2020
  Time: 21:34
 """

import time
from daemon import logger
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


class App:

    def __init__(self) -> None:
        super().__init__()
        self.df = pd.DataFrame()

    def start(self):
        while True:
            # Специфичная логика вашего приложения
            time.sleep(5)
            logger.info("some info")
            self.iteration()

    def iteration(self):
        page_container_class = '.bx-pagination-container ul li:nth-last-child(2) a span'

        url = 'https://www.mirea.ru/news/'  # url
        page_pattern = "?PAGEN_1=%s"
        r = requests.get(url)
        with open('test.html', 'w') as output_file:
            results = [self.read_db()]
            output_file.write(r.text)

            soup = BeautifulSoup(r.text, 'lxml')

            page_count = 2  # int(soup.select_one(page_container_class).text)
            print('page_count', page_count)
            for i in range(page_count):
                r = requests.get(url + page_pattern % (i + 1))
                html = r.text
                print('Parsing %d page' % (i + 1))
                page_results = self.parse_one_page(html)
                if len(page_results):
                    results.append(pd.DataFrame(page_results))
        if len(results):
            df = pd.concat(results, ignore_index=True)
            df.to_csv('results.csv', index=None)
        else:
            print('Empty results')

    def read_db(self):
        if self.df.empty and os.path.isfile('results.csv'):
            self.df = pd.read_csv('results.csv', index_col=None)

        return self.df

    def is_news_exists(self, href):
        df = self.read_db()
        if not ('href' in df.columns):
            return False
        found = df[df['href'] == href]
        return bool(len(found))

    def parse_one_page(self, text):
        results = []
        container_class = 'uk-grid-medium'
        soup = BeautifulSoup(text, 'lxml')
        news_container = soup.find('div', {'class': container_class})
        news_list = news_container.find_all('div', {'class': 'uk-card'})
        for news_item in news_list:
            result = self.parse_one_news(news_item)
            if result:
                results.append(result)
        return results

    def parse_one_news(self, news_item):
        href = news_item.find('a', {'class': 'uk-link-reset'}).get('href')
        if (self.is_news_exists(href)):
            return None
        title = news_item.find('a', {'class': 'uk-link-reset'}).text.strip()
        image = news_item.find('img').get('src')
        time = news_item.find('div', {'class': 'uk-h6'}).text.strip()
        return {
            'title': title,
            'href': href,
            'time': time,
            'image': image,
        }

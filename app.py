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
            logger.info("Parsing")
            self.iteration()

    def stop(self):
        logger.info("Daemon stop")

    def get_text(self, url):
        r = requests.get(url)
        return r.text

    def iteration(self):
        page_container_class = '.bx-pagination-container ul li:nth-last-child(2) a span'

        url = 'https://www.mirea.ru/news/'  # url
        page_pattern = "?PAGEN_1=%s"
        text = self.get_text(url)
        results = [self.read_db()]
        with open('/Users/antonvasilev/PyCharmProjects/bsbo__09_and_10__17/test.html', 'w') as output_file:
            output_file.write(text)

            soup = BeautifulSoup(text, 'lxml')

            page_count = 1  # int(soup.select_one(page_container_class).text)
            logger.info('page_count %d' % page_count)
            for i in range(page_count):
                html = self.get_text(url + page_pattern % (i + 1))
                logger.info('Parsing     %d page' % (i + 1))
                page_results = self.parse_one_page(html)
                if len(page_results):
                    results.append(pd.DataFrame(page_results))
        if len(results) > 1:
            df = pd.concat(results, ignore_index=True)
            logger.info('Save to file %d results' % df.count()[0])
            df.to_csv('/Users/antonvasilev/PyCharmProjects/bsbo__09_and_10__17/results.csv', index=None)
        else:
            logger.info('Empty results')

    def read_db(self):
        filepath = '/Users/antonvasilev/PyCharmProjects/bsbo__09_and_10__17/results.csv'
        if self.df.empty and os.path.isfile(filepath):
            self.df = pd.read_csv(filepath, index_col=None)

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

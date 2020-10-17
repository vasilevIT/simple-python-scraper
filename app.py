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
    def start(self):
        while True:
            # Специфичная логика вашего приложения
            time.sleep(5)
            self.load_page()

    def stop(self):
        pass

    def load_page(self):
        filename = '/Users/antonvasilev/PyCharmProjects/bsbo__09_and_10__17/results.csv'
        if os.path.isfile(filename):
            self.store = pd.read_csv(filename)
        else:
            self.store = pd.DataFrame()

        self.results = []
        url = 'https://www.mirea.ru/news/'
        response = requests.get(url)
        html = response.text

        bs = BeautifulSoup(html, 'lxml')
        container = bs.find('div', {'class': 'uk-grid-medium'})
        cards = container.find_all('div', {'class': 'uk-card'})
        for card in cards:
            self.parse_card(card)

        if len(self.results) > 0:
            df = pd.DataFrame(self.results)

            result_df = pd.concat([self.store, df])
            result_df.to_csv('/Users/antonvasilev/PyCharmProjects/bsbo__09_and_10__17/results.csv')

    def parse_card(self, card):
        img = card.find('img')
        link = card.find('a', {'class': 'uk-link-reset'})

        image_src = img.get('src')
        href = link.get('href')
        title = link.text
        date = card.find('div', {'class': 'uk-h6'}).text

        if not self.isExists(href):
            self.results.append({
                "href": href,
                "title": title,
                "date": date,
                "image_src": image_src
            })
            logger.info('New card ' + title)

    def isExists(self, href):
        if not ('href' in self.store.columns):
            return False
        found = self.store[self.store['href'] == href]
        return bool(found.count()[0])

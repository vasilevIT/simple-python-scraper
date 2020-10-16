"""
  Created by PyCharm.
  User: antonvasilev <bysslaev@gmail.com>
  Date: 16/10/2020
  Time: 21:34
 """

import time
from daemon import logger
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
class App:
    def start(self):
        while True:
            # Специфичная логика вашего приложения
            time.sleep(5)
            logger.info("some info")
            self.iteration()

    def iteration(self):
        container_class = 'js-load-container'
        url = 'https://www.rbc.ru/finances/'  # url
        r = requests.get(url)
        with open('test.html', 'w') as output_file:
            results = []
            output_file.write(r.text)
            soup = BeautifulSoup(r.text, 'lxml')
            news_container = soup.find('div', {'class': container_class})
            news_list = news_container.find_all('div', {'class': 'item'})
            for news_item in news_list :
                title = news_item.find('span', {'class': 'item__title'}).text.strip()
                href = news_item.find('a', {'class': 'item__link'}).get('href')
                image = news_item.find('img', {'class': 'item__image'}).get('src')
                time = news_item.find('span', {'class': 'item__category'}).text.strip()
                results.append({
                    'title': title,
                    'href': href,
                    'time': time,
                    'image': image,
                })

        df = pd.DataFrame(results)
        df.to_csv('results.csv')


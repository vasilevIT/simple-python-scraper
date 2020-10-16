"""
  Created by PyCharm.
  User: antonvasilev <bysslaev@gmail.com>
  Date: 16/10/2020
  Time: 21:34
 """

import time
from daemon import logger


class App:
    def start(self):
        while True:
            # Специфичная логика вашего приложения
            time.sleep(5)
            logger.info("some info")

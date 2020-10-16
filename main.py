"""
  Created by PyCharm.
  User: antonvasilev <bysslaev@gmail.com>
  Date: 16/10/2020
  Time: 21:34
 """


from daemon import *

from app import App
import time


class MyDaemon(Daemon):
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        super().__init__(pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null')
        # Инициализация класса по работе с БД

    def run(self):
        # Запуск парсинга
        self.application = App()
        self.application.start()


    def stop(self):
        self.application.stop()
        super().stop()

if __name__ == "__main__":
    daemon = MyDaemon(pid_file)

    if len(sys.argv) == 2:
        logger.info('{} {}'.format(sys.argv[0], sys.argv[1]))

        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        logger.warning('show cmd deamon usage')
        print("Usage: {} start|stop|restart".format(sys.argv[0]))
        sys.exit(2)

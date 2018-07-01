import time
from queue import Queue
from threading import Thread

from utils.utilFunction import validate_useful_proxy
from manager.ProxyManager import ProxyManager
from utils.LogHandler import LogHandler

FAIL_COUNT = 1  # 校验失败次数， 超过次数删除代理


class ProxyCheckThread(ProxyManager, Thread):
    def __init__(self, queue, item_dict):
        ProxyManager.__init__(self)
        Thread.__init__(self)
        self.log = LogHandler('proxy_check', file=False)  # 多线程同时写一个日志文件会有问题
        self.queue = queue
        self.item_dict = item_dict

    def run(self):
        self.db.change_table(self.useful_proxy_queue)
        while self.queue.qsize():
            proxy = self.queue.get()
            count = self.item_dict[proxy]
            if validate_useful_proxy(proxy):
                # 验证通过计数器减1
                if count and int(count) > 0:
                    self.db.put(proxy, num=int(count) - 1)
                else:
                    pass
                self.log.info('ProxyCheck: {} validation pass'.format(proxy))
            else:
                self.log.info('ProxyCheck: {} validation fail'.format(proxy))
                if count and int(count) + 1 >= FAIL_COUNT:
                    self.log.info('ProxyCheck: {} fail too many, delete!'.format(proxy))
                    self.db.delete(proxy)
                else:
                    self.db.put(proxy, num=int(count) + 1)
            self.queue.task_done()


class ProxyValidSchedule(ProxyManager, object):
    def __init__(self):
        ProxyManager.__init__(self)
        self.queue = Queue()
        self.proxy_item = dict()

    def __valid_proxy(self, threads=10):
        """
        验证useful_proxy代理
        """
        thread_list = list()
        for index in range(threads):
            thread_list.append(ProxyCheckThread(self.queue, self.proxy_item))

        for thread in thread_list:
            thread.daemon = True
            thread.start()

        for thread in thread_list:
            thread.join()

    def main(self):
        self.put_queue()  # 数据准备
        while True:
            if not self.queue.empty():
                self.log.info("Start valid useful proxy")
                self.__valid_proxy()
            else:
                self.log.info('Valid Complete! sleep 5 minutes.')
                time.sleep(60 * 5)  # 每隔5分钟校验一次
                self.put_queue()

    def put_queue(self):
        self.db.change_table(self.useful_proxy_queue)
        self.proxy_item = self.db.get_all()
        for item in self.proxy_item:
            self.queue.put(item)

    @staticmethod
    def run():
        schedule = ProxyValidSchedule()
        schedule.main()


if __name__ == '__main__':
    ProxyValidSchedule.run()

import time
import logging
from threading import Thread
from apscheduler.schedulers.blocking import BlockingScheduler

from manager.ProxyManager import ProxyManager
from utils.utilFunction import validate_useful_proxy
from utils.LogHandler import LogHandler

logging.basicConfig()


class ProxyRefreshSchedule(ProxyManager):
    """
    代理定时刷新
    """

    def __init__(self):
        ProxyManager.__init__(self)
        self.log = LogHandler('refresh_schedule')

    def valid_proxy(self):
        """
        验证raw_proxy_queue中的代理, 将可用的代理放入useful_proxy_queue
        """
        raw_proxy_item = self.db.pop_proxy(self.raw_proxy_queue)
        self.log.info('ProxyRefreshSchedule: %s start validProxy' % time.ctime())
        # 计算剩余代理，用来减少重复计算
        remaining_proxies = self.get_all()
        while raw_proxy_item:
            if (raw_proxy_item not in remaining_proxies) and validate_useful_proxy(raw_proxy_item):
                self.db.put_useful_proxy(raw_proxy_item)
                self.log.info('ProxyRefreshSchedule: %s validation pass' % raw_proxy_item)
            else:
                # 删除掉无用的代理的详情
                self.db.delete_proxy_info('proxy_info_%s' % raw_proxy_item.decode('utf-8'))
                self.log.info('ProxyRefreshSchedule: %s validation fail' % raw_proxy_item)
                raw_proxy_item = self.db.pop_proxy(self.raw_proxy_queue)
            remaining_proxies = self.get_all()
        self.log.info('ProxyRefreshSchedule: %s validProxy complete' % time.ctime())


def refresh_pool():
    refresh_schedule = ProxyRefreshSchedule()
    refresh_schedule.valid_proxy()


def build_refresh_thread(process_num=30):
    proxy_manger = ProxyManager()

    # 获取新代理
    proxy_manger.refresh()

    # 检验新代理
    thread_list = []
    for num in range(process_num):
        proc = Thread(target=refresh_pool, args=())
        thread_list.append(proc)

    for num in range(process_num):
        thread_list[num].daemon = True
        thread_list[num].start()

    for num in range(process_num):
        thread_list[num].join()


def run():
    build_refresh_thread()
    blocking_scheduler = BlockingScheduler()
    blocking_scheduler.add_job(build_refresh_thread, 'interval', minutes=10)  # 每10分钟抓取一次
    blocking_scheduler.start()


if __name__ == '__main__':
    run()

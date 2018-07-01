import random
from utils import EnvUtil
from db.DbClient import DbClient
from utils.GetConfig import GetConfig
from utils.LogHandler import LogHandler
from utils.utilFunction import verify_proxy_format
from proxy_getter.getFreeProxy import GetFreeProxy


class ProxyManager(object):
    def __init__(self):
        self.db = DbClient()  # 选用的存储设备
        self.config = GetConfig()  # 配置文件 ini
        self.raw_proxy_queue = 'raw_proxy'
        self.log = LogHandler('proxy_manager')  # **日志**
        self.useful_proxy_queue = 'useful_proxy'

    def refresh(self):
        """
        获取代理的ip, 并将其存放到原始的proxy当中
        """
        for proxyGetter in self.config.proxy_getter_functions:  # 获取配置文件proxyGetter内容
            # fetch
            proxy_set = set()
            try:
                self.log.info("{func}: fetch proxy start".format(func=proxyGetter))
                proxy_iter = [_ for _ in getattr(GetFreeProxy, proxyGetter.strip())()]  # GetFreeProxy,配置的代理
            except Exception as e:
                self.log.error("{func}: fetch proxy fail".format(func=proxyGetter))
                continue
            for proxy in proxy_iter:
                proxy = proxy.strip()
                if proxy and verify_proxy_format(proxy):  # 验证代理格式
                    self.log.info('{func}: fetch proxy {proxy}'.format(func=proxyGetter, proxy=proxy))
                    proxy_set.add(proxy)
                else:
                    self.log.error('{func}: fetch proxy {proxy} error'.format(func=proxyGetter, proxy=proxy))

            # store
            for proxy in proxy_set:
                self.db.change_table(self.useful_proxy_queue)
                if self.db.exists(proxy):
                    continue
                self.db.change_table(self.raw_proxy_queue)
                self.db.put(proxy)

    def get(self):
        """
        return a useful proxy
        """
        self.db.change_table(self.useful_proxy_queue)
        item_dict = self.db.get_all()
        if item_dict:
            return random.choice(list(item_dict.keys()))

        return None

    def delete(self, proxy):
        """
        delete proxy from pool
        """
        self.db.change_table(self.useful_proxy_queue)
        self.db.delete(proxy)

    def get_all(self):
        """
        get all proxy from pool as list
        """
        self.db.change_table(self.useful_proxy_queue)
        item_dict = self.db.get_all()
        return list(item_dict.keys()) if item_dict else list()

    def get_proxy_number(self):
        self.db.change_table(self.raw_proxy_queue)
        total_raw_proxy = self.db.get_number()
        self.db.change_table(self.useful_proxy_queue)
        total_useful_queue = self.db.get_number()
        return {'raw_proxy': total_raw_proxy, 'useful_proxy': total_useful_queue}


if __name__ == '__main__':
    pp = ProxyManager()
    pp.refresh()

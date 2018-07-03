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
            proxy_list = []
            try:
                self.log.info("{func}: fetch proxy start".format(func=proxyGetter))
                proxy_iter = [_ for _ in getattr(GetFreeProxy, proxyGetter.strip())()]  # GetFreeProxy,配置的代理
            except Exception as e:
                self.log.error("{func}: fetch proxy fail".format(func=proxyGetter))
                continue
            for proxy in proxy_iter:
                ip = proxy.get('ip').strip()
                if proxy and verify_proxy_format(ip):  # 验证代理格式
                    self.log.info('{func}: fetch proxy {proxy}'.format(func=proxyGetter, proxy=ip))
                    proxy_list.append(proxy)
                else:
                    self.log.error('{func}: fetch proxy {proxy} error'.format(func=proxyGetter, proxy=ip))

            # store
            for proxy in proxy_list:
                if self.db.is_exists_proxy(self.useful_proxy_queue, proxy.get('ip')):
                    continue
                self.db.put_raw_proxy(proxy)

    def get(self):
        """
        return a useful proxy
        """
        return self.db.get_random_proxy(self.useful_proxy_queue)

    def get_all(self):
        """
        get all proxy from pool as list
        """
        return self.db.get_al1_proxy(self.useful_proxy_queue)

    def get_proxy_number(self):
        total_raw_proxy = len(self.db.get_al1_proxy(self.raw_proxy_queue))
        total_useful_queue = len(self.db.get_al1_proxy(self.useful_proxy_queue))

        return {'raw_proxy': total_raw_proxy, 'useful_proxy': total_useful_queue}


if __name__ == '__main__':
    pp = ProxyManager()
    pp.refresh()

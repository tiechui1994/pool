import os
import sys

from utils.GetConfig import GetConfig
from utils.utilClass import Singleton

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class DbClient(object, metaclass=Singleton):
    """
    数据结构设计:
        proxy_info_{ip}: hash 存储ip信息(ip, count, from) 在获取原始ip的时候存入. 删除的时机:
            1. 当原始的ip验证失败
            2. 重写校验useful_proxy时, ip失效

        raw_proxy: set 通过爬虫获取到的原始ip. 校验的时候删除之.
        useful_proxy: set  验证之后的ip
    """

    def __init__(self):
        self.config = GetConfig()
        self.__init_db_client()

    def __init_db_client(self):
        __type = None
        if "REDIS" == self.config.db_type:
            __type = "RedisClient"
        assert __type, 'type error, Not support db type: {}'.format(self.config.db_type)
        self.client = getattr(__import__(__type), __type)(host=self.config.db_host,
                                                          port=self.config.db_port)

    def get_random_proxy(self, name):
        return self.client.get_random_proxy(name)

    def get_al1_proxy(self, name):
        return self.client.get_al1_proxy(name)

    def put_useful_proxy(self, proxy):
        return self.client.put_useful_proxy(proxy)

    def put_raw_proxy(self, proxy_info_map):
        return self.client.put_raw_proxy(proxy_info_map)

    def pop_proxy(self, name):
        return self.client.pop_proxy(name)

    def delete_proxy_info(self, key):
        return self.client.delete_proxy_info(key)

    def delete_proxy(self, name, ip):
        return self.client.delete_proxy(name, ip)

    def get_all_useful_proxy_info(self):
        return self.client.get_all_useful_proxy_info()

    def inckey(self, name, key, value):
        return self.client.inckey(name, key, value)

    def is_exists_proxy(self, name, value):
        return self.client.is_exists_proxy(name, value)

    def clear_all_data(self):
        return self.client.clear_all_data()


if __name__ == "__main__":
    pass

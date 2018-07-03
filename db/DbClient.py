import os
import sys

from utils.GetConfig import GetConfig
from utils.utilClass import Singleton

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class DbClient(object, metaclass=Singleton):
    """
    DbClient DB工厂类 提供get/put/pop/delete/getAll/changeTable方法

    目前存放代理的table/collection/hash有两种：
        raw_proxy： 存放原始的代理；
        useful_proxy_queue： 存放检验后的代理；

        所有方法需要相应类去具体实现：
            SSDB：SsdbClient.py
            REDIS:RedisClient.py

    """

    def __init__(self):
        self.config = GetConfig()
        self.__init_db_client()

    def __init_db_client(self):
        __type = None
        if "REDIS" == self.config.db_type:
            __type = "RedisClient"
        assert __type, 'type error, Not support db type: {}'.format(self.config.db_type)
        self.client = getattr(__import__(__type), __type)(name=self.config.db_name,
                                                          host=self.config.db_host,
                                                          port=self.config.db_port)

    def get_random_proxy(self, name):
        return self.client.get_random_proxy(name)

    def get_al1_proxy(self, name):
        return self.client.get_al1_proxy(name)

    def put_userful_proxy(self, proxy):
        return self.client.put_userful_proxy(proxy)

    def put_raw_proxy(self, proxy_info_map):
        return self.client.put_raw_proxy(proxy_info_map)

    def get_proxy_info_by_ip(self, ip):
        return self.client.get_proxy_info_by_ip(ip)

    def pop_proxy(self, name):
        return self.client.pop_proxy(name)

    def delete_proxy_info(self, key):
        return self.client.delete_proxy_info(key)

    def get_all_userful_proxy_info(self):
        return self.client.get_all_userful_proxy_info()

    def inckey(self, name, key, value):
        return self.client.inckey(name, key, value)

    def is_exists_proxy(self, name, value):
        return self.client.is_exists_proxy(name, value)


if __name__ == "__main__":
    pass

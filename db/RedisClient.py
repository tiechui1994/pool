import random
import redis

"""
数据结构设计:
    proxy_info_{ip}: hash 存储ip信息(ip, count, from)
    raw_proxy: set 原始的ip
    useful_proxy: set  存储验证后的ip
"""


class RedisClient(object):
    def __init__(self, name, host, port):
        self.name = name
        self.__conn = redis.Redis(host=host, port=port, db=0)

    def get_random_proxy(self, name):
        member = random.choice(self.__conn.smembers(name))
        return member.decode('utf-8')

    def get_al1_proxy(self, name):
        return self.__conn.smembers(name)

    def put_useful_proxy(self, proxy):
        return self.__conn.sadd('useful_proxy', proxy)

    def put_raw_proxy(self, proxy_info_map):
        proxy_ip = proxy_info_map.get('ip', None)

        if not proxy_ip:
            raise TypeError('Missing parameter proxy')

        pipeline = self.__conn.pipeline()
        pipeline.hmset('proxy_info_%s' % proxy_ip, proxy_info_map)
        pipeline.sadd('raw_proxy', proxy_ip)
        pipeline.execute()

    def get_all_useful_proxy_info(self):
        if self.__conn.exists('raw_proxy') and self.__conn.scard('raw_proxy') > 0:
            items = self.__conn.sort('raw_proxy', by='xx', get=['proxy_info_*->ip', 'proxy_info_*->count'], groups=True)

            return list(map(lambda item: {'ip': str(item[0]), 'count': int(item[1])}, items))

        return []

    def pop_proxy(self, name):
        return self.__conn.spop(name)

    def delete_proxy_info(self, key):
        return self.__conn.delete(key)

    def delete_proxy(self, name, ip):
        return self.__conn.srem(name, [ip])

    def inckey(self, name, key, value):
        self.__conn.hincrby(name, key, value)

    def is_exists_proxy(self, name, value):
        return self.__conn.sismember(name, value)

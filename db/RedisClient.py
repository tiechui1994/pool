import json
import random

import array
import redis
from utils.utilFunction import verify_proxy_format

"""
数据结构设计:
    proxy_info_{ip}: hash 存储ip信息(ip, count, from)
    raw_proxy: set 原始的ip
    userful_proxy: set  存储验证后的ip
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

    def put_userful_proxy(self, proxy):
        return self.__conn.sadd('userful_proxy', proxy)

    def put_raw_proxy(self, proxy_info_map):
        proxy_ip = proxy_info_map.get('ip', None)

        if not proxy_ip:
            raise TypeError('Missing parameter proxy')

        pipeline = self.__conn.pipeline()
        pipeline.hmset('proxy_info_%s' % proxy_ip, proxy_info_map)
        pipeline.sadd('raw_proxy', proxy_ip)
        pipeline.execute()

    def get_proxy_info_by_ip(self, ip):
        if not ip or not verify_proxy_format(ip):
            raise TypeError('Ip does not meet the requirements')

        return self.__conn.hgetall('proxy_info_%s' % ip)

    def get_all_userful_proxy_info(self):
        items = self.__conn.sort('raw_proxy', by='xx', get=['proxy_info_*->ip', 'proxy_info_*->count'], groups=True)

        return list(map(lambda item: {'ip': str(item[0]), 'count': int(item[1])}, items))

    def pop_proxy(self, name):
        return self.__conn.spop(name)

    def delete_proxy_info(self, key):
        return self.__conn.delete(key)

    def inckey(self, name, key, value):
        self.__conn.hincrby(name, key, value)

    def is_exists_proxy(self, name, value):
        return self.__conn.sismember(name, value)


if __name__ == '__main__':
    redis_con = RedisClient('proxy', 'localhost', 6399)
    # proxy = {
    #     'proxy': '%d.%d.%d.%d:%d' % (
    #         random.randint(10, 255), random.randint(10, 255),
    #         random.randint(10, 255), random.randint(10, 255),
    #         random.randint(10, 10000)),
    #     'from': ''.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyz', 5)),
    #     'count': random.randint(1, 3)
    # }
    # redis_con.put_raw_proxy(proxy)
    #
    # res = redis_con.get_proxy_info_by_ip(proxy.get('proxy'))
    # print(res, res.get(b'count'))

    print(redis_con.get_all_userful_proxy_info())
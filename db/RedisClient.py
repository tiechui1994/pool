import json
import random
import redis


class RedisClient(object):
    def __init__(self, name, host, port):
        self.name = name
        self.__conn = redis.Redis(host=host, port=port, db=0)

    def get(self):
        """
        get random result
        """
        key = self.__conn.hgetall(name=self.name)
        rkey = random.choice(list(key.keys())) if key else None
        if isinstance(rkey, bytes):
            return rkey.decode('utf-8')
        else:
            return rkey

    def put(self, key):
        """
        put an item
        """
        key = json.dumps(key) if isinstance(key, (dict, list)) else key
        return self.__conn.hincrby(self.name, key, 1)

    def getvalue(self, key):
        value = self.__conn.hget(self.name, key)
        return value if value else None

    def pop(self):
        """
        pop an item
        """
        key = self.get()
        if key:
            self.__conn.hdel(self.name, key)
        return key

    def delete(self, key):
        """
        delete an item
        """
        self.__conn.hdel(self.name, key)

    def inckey(self, key, value):
        self.__conn.hincrby(self.name, key, value)

    def get_all(self):
        return [key.decode('utf-8') for key in self.__conn.hgetall(self.name).keys()]

    def get_status(self):
        return self.__conn.hlen(self.name)

    def change_table(self, name):
        self.name = name

    def exists(self, key, **kwargs):
        return self.__conn.exists(key)


if __name__ == '__main__':
    redis_con = RedisClient('proxy', 'localhost', 6379)
    redis_con.change_table('raw_proxy')
    redis_con.pop()
    print(redis_con.get_status())
    print(redis_con.get_all())

import os
from utils.utilClass import ConfigParse
from utils.utilClass import LazyProperty


class GetConfig(object):
    """
    to get config from config.ini
    """

    def __init__(self):
        self.pwd = os.path.split(os.path.realpath(__file__))[0]
        self.config_path = os.path.join(os.path.split(self.pwd)[0], 'Config.ini')
        self.config_file = ConfigParse()
        self.config_file.read(self.config_path)

    @LazyProperty
    def db_type(self):
        return self.config_file.get('db', 'type')

    @LazyProperty
    def db_name(self):
        return self.config_file.get('db', 'name')

    @LazyProperty
    def db_host(self):
        return self.config_file.get('db', 'host')

    @LazyProperty
    def db_port(self):
        return int(self.config_file.get('db', 'port'))

    @LazyProperty
    def proxy_getter_functions(self):
        return self.config_file.options('ProxyGetter')

    @LazyProperty
    def host_ip(self):
        return self.config_file.get('HOST','ip')

    @LazyProperty
    def host_port(self):
        return int(self.config_file.get('HOST', 'port'))

if __name__ == '__main__':
    gg = GetConfig()
    print(gg.db_type)
    print(gg.db_name)
    print(gg.db_host)
    print(gg.db_port)
    print(gg.proxy_getter_functions)
    print(gg.host_ip)
    print(gg.host_port)

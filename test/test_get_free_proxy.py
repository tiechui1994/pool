from proxy_getter.getFreeProxy import GetFreeProxy
from utils.GetConfig import GetConfig


def test_get_free_proxy():
    """
    test class GetFreeProxy in proxy_getter/GetFreeProxy
    """
    gc = GetConfig()
    proxy_getter_functions = gc.proxy_getter_functions
    for proxyGetter in proxy_getter_functions:
        proxy_count = 0
        for proxy in getattr(GetFreeProxy, proxyGetter.strip())():
            if proxy:
                print('{func}: fetch proxy {proxy},proxy_count:{proxy_count}'.format(func=proxyGetter, proxy=proxy,
                                                                                     proxy_count=proxy_count))
                proxy_count += 1
                # assert proxy_count >= 20, '{} fetch proxy fail'.format(proxyGetter)


if __name__ == '__main__':
    test_get_free_proxy()

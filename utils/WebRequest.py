from urllib3 import PoolManager
import random

from utils.utilClass import Singleton

"""
典型的爬虫案例
"""


class WebRequest(object, metaclass=Singleton):
    def __init__(self):
        self.pool = PoolManager()

    @property
    def user_agent(self):
        """
        return an User-Agent at random
        :return:
        """
        ua_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        ]
        return random.choice(ua_list)

    @property
    def header(self):
        """
        basic header
        :return:
        """
        return {'User-Agent': self.user_agent,
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'Accept-Language': 'en-US,en;q=0.9'}

    def get(self, url, header=None, retry_time=5,
            timeout=30, encoding='utf-8'):
        """
        get method
        :param url: target url
        :param header: headers
        :param retry_time: retry time when network error
        :param timeout: network timeout
        :param retry_interval: retry interval(second)
        :param encoding: 'utf-8'
        :return:
        """
        headers = self.header
        if header and isinstance(header, dict):
            headers.update(header)
        while True:
            try:
                response = self.pool.request('GET', url, headers=headers,
                                             timeout=timeout, retries=retry_time)
                print(response.data)
                html = response.data.decode(encoding)
                status = response.status
                if status in range(500, 510):
                    raise Exception
                return html
            except Exception as e:
                print(e)
                return ''


if __name__ == '__main__':
    req_url = 'http://www.goubanjia.com/'
    webreq = WebRequest()
    print(webreq.get(req_url))

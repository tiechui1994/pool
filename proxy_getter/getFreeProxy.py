import re
import urllib3
from utils.utilFunction import get_html_tree
from utils.WebRequest import WebRequest

urllib3.disable_warnings()  # urlib3的一个方法

"""
爬虫获取以下的代理服务IP:
    66ip.cn
    data5u.com
    xicidaili.com
    goubanjia.com
    xdaili.cn
    kuaidaili.com
    cn-proxy.com
    proxy-list.org
    www.mimiip.com to do
"""


class GetFreeProxy(object):
    @staticmethod
    def free_proxy_one(area=33, page=1):
        """
        代理66 http://www.66ip.cn/
        :param area: 抓取代理页数，page=1北京代理页，page=2上海代理页......
        """
        area = 33 if area > 33 else area
        for area_index in range(1, area + 1):
            for i in range(1, page + 1):
                url = "http://www.66ip.cn/areaindex_{}/{}.html".format(area_index, i)
                html_tree = get_html_tree(url, encoding='gbk')
                tr_list = html_tree.xpath("//*[@id='footer']/div/table/tr[position()>1]")
                if len(tr_list) == 0:
                    continue
                for tr in tr_list:
                    yield {
                        'ip': tr.xpath("./td[1]/text()")[0] + ":" + tr.xpath("./td[2]/text()")[0],
                        'from': '66ip',
                        'count': 0
                    }
                break

    @staticmethod
    def free_proxy_two(page_count=2):
        """
        西刺代理 http://www.xicidaili.com
        :return:
        """
        url_list = [
            'http://www.xicidaili.com/nn/',  # 高匿
            'http://www.xicidaili.com/nt/',  # 透明
        ]
        for each_url in url_list:
            for i in range(1, page_count + 1):
                page_url = each_url + str(i)
                tree = get_html_tree(page_url)
                proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in proxy_list:
                    try:
                        yield {
                            'ip': ':'.join(proxy.xpath('./td/text()')[0:2]),
                            'from': 'xicidaili',
                            'count': 0
                        }
                    except Exception as e:
                        pass

    @staticmethod
    def free_proxy_three():
        """
        guobanjia http://www.goubanjia.com/
        :return:
        """
        url = "http://www.goubanjia.com/"
        tree = get_html_tree(url)
        proxy_list = tree.xpath('//td[@class="ip"]')
        # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
        # 需要过滤掉<p style="display:none;">的内容
        xpath_str = """.//*[not(contains(@style, 'display: none'))
                                        and not(contains(@style, 'display:none'))
                                        and not(contains(@class, 'port'))
                                        ]/text()
                                """
        for each_proxy in proxy_list:
            try:
                # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
                ip_addr = ''.join(each_proxy.xpath(xpath_str))
                port = each_proxy.xpath(".//span[contains(@class, 'port')]/text()")[0]
                yield {
                    'ip': '{}:{}'.format(ip_addr, port),
                    'from': 'goubanjia',
                    'count': 0
                }
            except Exception as e:
                pass

    @staticmethod
    def free_proxy_four():
        """
        快代理 https://www.kuaidaili.com
        """
        url_list = [
            'https://www.kuaidaili.com/free/inha/{page}/',
            'https://www.kuaidaili.com/free/intr/{page}/'
        ]
        for url in url_list:
            for page in range(1, 5):
                page_url = url.format(page=page)
                tree = get_html_tree(page_url)
                proxy_list = tree.xpath('.//table//tr')
                for tr in proxy_list[1:]:
                    yield {
                        'ip': ':'.join(tr.xpath('./td/text()')[0:2]),
                        'from': 'kuaidaili',
                        'count': 0
                    }

    @staticmethod
    def free_proxy_five():
        """
        码农代理 https://proxy.coderbusy.com/
        """
        urls = ['https://proxy.coderbusy.com/classical/country/cn.aspx?page=1']
        request = WebRequest()
        for url in urls:
            html = request.get(url)
            proxies = re.findall('data-ip="(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})".+?>(\d+)</td>', html)
            for proxy in proxies:
                yield {
                    'ip': ':'.join(proxy),
                    'from': 'coderbusy',
                    'count': 0
                }

    @staticmethod
    def free_proxy_six():
        """
        云代理 http://www.ip3366.net/free/
        """
        urls = ['http://www.ip3366.net/free/']
        request = WebRequest()
        for url in urls:
            html = request.get(url)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', html)
            for proxy in proxies:
                yield {
                    'ip': ':'.join(proxy),
                    'from': 'ip3366',
                    'count': 0
                }

    @staticmethod
    def free_proxy_seven():
        """
        IP海 http://www.iphai.com/free/ng
        """
        urls = [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/wp'
        ]
        request = WebRequest()
        for url in urls:
            html = request.get(url)
            proxies = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
                                 html)
            for proxy in proxies:
                yield {
                    'ip': ":".join(proxy),
                    'from': 'iphais',
                    'count': 0
                }

    @staticmethod
    def free_proxy_eight(page_count=8):
        """
        guobanjia http://ip.jiangxianli.com/?page=
        免费代理库, 超多量
        """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?page={}'.format(i)
            html_tree = get_html_tree(url)
            tr_list = html_tree.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr")
            if len(tr_list) == 0:
                continue
            for tr in tr_list:
                yield {
                    'ip': tr.xpath("./td[2]/text()")[0] + ":" + tr.xpath("./td[3]/text()")[0],
                    'from': 'jiangxianli',
                    'count': 0
                }

    @staticmethod
    def free_proxy_wall_one():
        """
        墙外网站 cn-proxy
        """
        urls = ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
        request = WebRequest()
        for url in urls:
            html = request.get(url)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', html)
            for proxy in proxies:
                yield {
                    'ip': ':'.join(proxy),
                    'from': 'proxy',
                    'count': 0
                }

    @staticmethod
    def free_proxy_wall_two():
        """
        https://proxy-list.org/english/index.php
        """
        urls = ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, 10)]
        request = WebRequest()
        import base64
        for url in urls:
            html = request.get(url)
            proxies = re.findall(r"Proxy\('(.*?)'\)", html)
            for proxy in proxies:
                yield {
                    'ip': base64.b64decode(proxy).decode(),
                    'from': 'english',
                    'count': 0
                }

    @staticmethod
    def free_proxy_wall_three():
        urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1']
        request = WebRequest()
        for url in urls:
            html = request.get(url, retry_time=3)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', html)
            for proxy in proxies:
                yield {
                    'ip': ':'.join(proxy),
                    'from': 'proxylistplus',
                    'count': 0
                }


if __name__ == '__main__':
    proxy_iter = GetFreeProxy.free_proxy_wall_one()
    for proxy_ip in proxy_iter:
        print(proxy_ip)

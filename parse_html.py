import json
import tempfile
import requests
import time

import bs4

""""
bs4.BeautifulSoup(html, "lxml")

find_all(name="a", attrs={"class":"", "href":""}, text=".*") // 所有的 <a> 标签

find(name="div", attrs={"class":""}) // 第一个 <div> 标签
"""


def html_parse():
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/86.0.4240.198 Safari/537.36"
    }
    url = "https://www.tvmao.com/program/NMGTV/NMGTV7"
    response = requests.request("GET", url=url, headers=header)
    soup = bs4.BeautifulSoup(response.content, "lxml")
    tokens = soup.find_all(name="div", attrs={'class': 'over_hide'})

    data = {
        "channel": "内蒙古电视台蒙语卫视",
        "items": [],
    }
    for val in tokens:
        t = val.find(attrs={'class': 'am'}).text
        v = val.find(attrs={'class': 'p_show'}).text
        data["items"].append({
            "start": int(time.mktime(time.strptime('2021-01-05 ' + t, "%Y-%m-%d %H:%M"))),
            "end": 0,
            "name": v
        })

    with tempfile.TemporaryFile("w", encoding='utf-8') as fd:
        fd.write(json.dumps(data, ensure_ascii=False))
        print(json.dumps(data, ensure_ascii=False))


html_parse()

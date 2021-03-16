# -*- coding: utf-8 -*-
"""
@Time ： 2021/3/12
@Auth ： zhangqimin
@File ：web_url.py
@IDE ：PyCharm

"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup as Bs4

head_url = "https://wx.guorou.net"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}
def get_first_url():
    list_href = []
    reaponse = requests.get(head_url, headers=headers)
    print(reaponse.text)
    soup = Bs4(reaponse.text, "lxml")
    urls_li = soup.select("#__next > div > div > header > div > div > div")
    print(urls_li)
    for url_li in urls_li:
        urls = url_li.select("a")
        for url in urls:
            url_href = url.get("href")
            list_href.append(head_url+url_href)
            out_url = list(set(list_href))
            print(out_url)
    return out_url


def get_next_url(urllist):
    url_list = []
    for url in urllist:
        response = requests.get(url,headers=headers)
        soup = Bs4(response.text,"lxml")
        urls = soup.find_all("a")
        if urls:
            for url2 in urls:
                url2_1 = url2.get("href")
                if url2_1:
                    if url2_1[0] == "/":
                        url2_1 = head_url + url2_1
                        url_list.append(url2_1)
                        if url2_1[0:24] == "https://wx.guorou.net":
                            url2_1 = url2_1
                            url_list.append(url2_1)
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
        else:
            pass
    url_list2 = set(url_list)
    for url_ in url_list2:
        res = requests.get(url_)
        if res.status_code ==200:
            print(url_)
    print(len(url_list2))
    get_next_url(url_list2)


def getAllUrl(url):
        import urllib.request
        from bs4 import BeautifulSoup
        html = urllib.request.urlopen(url).read().decode("utf-8")
        soup = BeautifulSoup(html, features='html.parser')
        tags = soup.find_all('a')
        for tag in tags:
            print(str(tag.get('href')).strip())


if __name__ == "__main__":
    # urllist = get_first_url()
    # get_next_url(urllist)
    getAllUrl("https://wx.guorou.net/")
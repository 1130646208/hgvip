#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/2/11 21:48
# @Author  : wsx
# @Site    : 
# @File    : proxy_test.py
# @Software: PyCharm

from crawl_movies import *
import requests
import re


def get(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
    }
    ip = ['39.106.223.207:80', '112.195.121.250:9999', '124.239.216.14:8060']
    proxies = {
        "http": "http://" + ip[2],
    }

    try:
        response = requests.get(url, headers=headers, timeout=20, proxies=proxies)
        if response.status_code == 200:
            print('请求成功,耗时:[%s]秒.' % response.elapsed.seconds)
            return response.text
        else:
            print('请求出错啦.代码:[%s]' % response.status_code)
            return None
    except RequestException as e:
        print('请求出错啦.信息:[%s]' % e)
        return None



if __name__ == '__main__':
    page = get('http://service.cstnet.cn/ip')
    print(re.search(r'ip-num.*?>(.*?)<sup', page, re.S).group(1))


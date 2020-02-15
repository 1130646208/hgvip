#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/2/5 22:54
# @Author  : wsx
# @Site    : 更新所有类别
# @File    : main3.py
# @Software: PyCharm
# 多线程测试

# -*- coding: utf-8 -*-
from save_to_database import *
from crawl_movies import *
import re
from main2 import get_start
import time


def main():
    isdigit = re.compile(r'\d+')
    s = Save()
    g = Get()
    exist_ids = set()
    # 检查数据库中已经存在的类别
    print('<已完成类别>')
    for each in s.check_classes():
        id = each.split('_')[-1]
        if re.match(isdigit, id):
            exist_ids.add(id)
            print(id, end=' ')
    # 请求服务器所有的类别, 并检查哪些类别还没有压榨
    print('\n<未完成类别>')
    for each in g.get_cate():
        id = each['clsid']
        if not str(id) in exist_ids:
            page = g.get_page_num(id)
            print('[id:%s(%s) <%s 页>]' % (id, each['类别'], page), end=' ')
            # time.sleep(3)
            # get_start(id)


if __name__ == '__main__':
    main()

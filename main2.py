#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/2/5 19:25
# @Author  : wsx
# @desc    : 多线程爬取一个类别数据, 更新到数据库中, 线程数在config.py中
# @File    : main2.py
# @Software: PyCharm

from save_to_database import *
import queue
import time
from config import *


def get_start(cls_id):
    start = time.time()

    g = Get()
    print('Getting class total pages...')
    pages = g.get_page_num(cls_id)
    print('Total [%s] pages' % pages)
    print('Getting movies...')
    q = queue.Queue(maxsize=MAX_THREADS)
    threads = []
    for page in range(int(pages)):
        q.put(0)  # 队列没有起到传参作用, 只是为了控制线程个数而引入的
        u = Update(cls_id, page + 1, q)
        threads.append(u)
        u.start()
    q.join()  # 等待主线程结束, 方便计时

    end = time.time()
    print('*程序结束, 共耗时:[%.2f]s' % (end - start))
    # 统计所有线程成功,失败的数量
    print('*共插入数据:成功:[%s]条, 失败[%s]条.' % (sum([x.succeed for x in threads]), sum([x.failed for x in threads])))


def main():
    cls_id = input('请输入类别id:')
    get_start(cls_id)


if __name__ == '__main__':
    main()

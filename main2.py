#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/2/5 19:25
# @Author  : wsx
# @desc    : 多线程爬取网站数据, 更新到数据库中, 线程数在config.py中
# @File    : main2.py
# @Software: PyCharm


from crawl_movies import Get
from save_to_database import Save
from threading import Thread
import queue
import time
from config import *


class Update(Thread):
    def __init__(self,cls_id, page, queue):
        Thread.__init__(self)
        self.queue = queue
        self.cls_id = cls_id
        self.page = page
        self.g = Get()
        self.s = Save()
        self.succeed = 0
        self.failed = 0

    def update_cate(self):
        cates = self.g.get_cate()
        for each in self.s.save_many_to_mongo(cates, collection_name='classes', ins=False):
            print(each)

    def update_class(self):
        success = 0
        fail = 0
        cls_id = self.cls_id
        page = self.page
        print('Updating page %s.\n' % page)
        for each in self.s.save_many_to_mongo(self.g.get_mov_info(cls_id, page), collection_name='class_' + cls_id, ins=True):
            if each:
                success += 1
            else:
                fail += 1
        print('Page %s update ok.\n' % page)
        self.failed = fail
        self.succeed = success
        # 完成后再取出元素
        self.queue.task_done()
        self.queue.get()

    def run(self):
        self.update_class()


if __name__ == '__main__':
    start = time.time()

    g = Get()
    cls_id = input('请输入类别id:')
    print('Getting class total pages...')
    pages = g.get_page_num(cls_id)
    print('Total [%s] pages' % pages)
    print('Getting movies...')
    q = queue.Queue(maxsize=MAX_THREADS)
    threads = []
    for page in range(int(pages)):
        q.put(0)  # 队列没有起到传参作用, 只是为了控制线程个数而引入的
        u = Update(cls_id, page+1, q)
        threads.append(u)
        u.start()
    q.join()  # 等待主线程结束, 方便计时

    end = time.time()
    print('*程序结束, 共耗时:[%.2f]s' % (end-start))
    # 统计所有线程成功,失败的数量
    print('*共插入数据:成功:[%s]条, 失败[%s]条.' % (sum([x.succeed for x in threads]), sum([x.failed for x in threads])))

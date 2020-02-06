#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/2/5 19:25
# @Author  : wsx
# @Site    : 
# @File    : main2.py
# @Software: PyCharm
# 多线程爬取
from crawl_movies import Get
from save_to_database import Save
from threading import Thread
import queue
import time


class Update(Thread):
    def __init__(self,cls_id, page, queue):
        Thread.__init__(self)
        self.queue = queue
        self.cls_id = cls_id
        self.page = page
        self.g = Get()
        self.s = Save()
        self.success = 0
        self.failed = 0

    # def update_cate(self):
    #     g = Get()
    #     s = Save()
    #     cates = g.get_cate()
    #     for cate in s.save_many_to_mongo(cates, collection_name='classes', ins=False):
    #         pass

    def update_class(self):
        cls_id = self.cls_id
        page = self.page
        print('Updating page %s.\n' % page)
        for each in self.s.save_many_to_mongo(self.g.get_mov_info(cls_id, page), collection_name='class_' + cls_id, ins=True):
            if each:
                self.success += 1
            else:
                self.failed += 1
        print('Page %s update ok.\n' % page)
        # 完成后再取出元素
        self.queue.task_done()
        self.queue.get()

    def run(self):
        self.update_class()


if __name__ == '__main__':
    start = time.time()
    success = 0
    failed = 0

    g = Get()
    cls_id = input('类别id')
    pages = g.get_page_num(cls_id)
    q = queue.Queue(maxsize=10)  # 队列没有起到传参作用, 只是为了控制线程个数二引入的
    for page in range(int(pages)):
        q.put(page)
        u = Update(cls_id, page+1, q)
        u.start()

    end = time.time()
    print('程序结束, 共耗时:[%s]s' % (end-start))
    # print('插入数据:成功:[%s]条, 失败[%s]条.' % (success, failed))


#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/2/5 22:54
# @Author  : wsx
# @Site    : 
# @File    : main3.py
# @Software: PyCharm
# 多线程测试

# -*- coding: utf-8 -*-
import threading
import queue
import time
import random
maxThreads = 5


class Store(threading.Thread):
    def __init__(self, store, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.store = store

    def run(self):
        time.sleep(2)
        self.queue.get()
        self.queue.task_done()
        # print('This is store %s\n' % self.store)
        print('this is thread:%s' % self.name)


def main():
    q = queue.Queue(maxThreads)
    for i in range(15):
        s = Store(1, q)
        q.put(i)
        print(id(s))
        s.start()
    print('队列中还有未完成任务:', q.unfinished_tasks)
    q.join()
    print('over')


if __name__ == '__main__':
    main()

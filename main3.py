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
        try:
            print('This is store %s\n' % self.store)

            time.sleep(random.randint(1, 4))
        except Exception as e:
            print(e)
        finally:
            self.queue.get()
            self.queue.task_done()


def main():
    q = queue.Queue(maxThreads)

    for s in range(15):
        q.put(s)
        t = Store(s, q)
        t.start()
        print('队列中还有:', q.unfinished_tasks)
        # if s % 5 == 0:
        #     q.join()
    print('over')


if __name__ == '__main__':
    main()

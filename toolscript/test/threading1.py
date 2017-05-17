# coding=utf-8
__author__ = 'xuxin'

import threading
import time
# 方法1：将要执行的方法作为参数传给Thread的构造方法
n = 0
def func(n):
    while True:
        time.sleep(1)
        print 'func() passed to Thread:',n
def data():
    global n
    while True:
        time.sleep(1)
        n  = n+1


t1 = threading.Thread(target=func,args=(n,))
t2 = threading.Thread(target=data)
print t1
if t1:
    print '11111111111'
else:
    print '22222222222'
print 'b_t1.getName() = ',t1.getName()
print 'b_t2.getName() = ',t2.getName()
# t1.setDaemon(True)
t1.start()
t2.start()
t1.join(5)
print 'timeout:1'
print 't1.getName() = ',t1.getName()
print 't2.getName() = ',t2.getName()
print t1.isAlive()
# t1 = threading.Thread(target=func)
# t1.start()
# print 'a_t1.getName() = ',t1.getName()
# print 'a_t2.getName() = ',t2.getName()

# t3 = threading.Timer()

# # 方法2：从Thread继承，并重写run()
# class MyThread(threading.Thread):
#     def run(self):
#         print 'MyThread extended from Thread'
#
# t = MyThread()
# t.start()

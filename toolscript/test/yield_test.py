# coding=gb2312
__author__ = 'xuxin'

def h():
    #测试
    print 'test1'
    yield 5
    print 'test2'

c = h()
# c.next()
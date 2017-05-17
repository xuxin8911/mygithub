# coding=utf-8
__author__ = 'xuxin'
import json
import traceback
def func1():
    try:
        print 'try...'
        a = 2/0
        return 'result try...'
    except Exception,e:
        print 'except...'
        print Exception,type(Exception)
        print e,type(e)
        print traceback.format_exc(1)
    finally:
        print 'finally...'
        return 'result finally...'

def assert_test():
    try:
        assert 1 == 2
    except AssertionError,e:
        print AssertionError
        print e
    print 'assert test...'
    return 'result assert...'

if __name__ == '__main__':
    # ret = func1()
    # print ret
    ret = assert_test()
    print ret

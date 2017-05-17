# coding=utf-8
__author__ = 'xuxin'

from twisted.internet import reactor
import time
def print_test():
    print 'test'

if __name__ == '__main__':
    reactor.callLater(1,print_test)
    reactor.run()
    reactor.stop()
    for i in range(10):
        print i
        time.sleep(1)


# coding=utf-8
__author__ = 'xuxin'

from twisted.internet import defer,reactor
import time

class Getter:
    def getData(self,x):
        d = defer.Deferred()
        reactor.callLater(10,d.callback,x*3)
        print 'line 11'
        return d

def printData(d):
    print 'line 14'
    print d

if __name__== '__main__':
    t1 = time.time()
    g = Getter()
    d = g.getData(3)
    print 'line 19'
    d.addCallback(printData)
    print 'line 21'
    reactor.callLater(4,reactor.stop)
    print 'line 23'
    reactor.run()
    print 'line 25'
    print time.time() - t1

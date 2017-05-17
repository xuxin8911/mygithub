#coding=utf-8
__author__ = 'xuxin'
from twisted.internet import protocol, reactor
from time import ctime
PORT = 8087

class TSServProtocol(protocol.Protocol):
    def connectionMade(self):
        clnt = self.clnt = self.transport.getPeer().host
        print '...connected from:', clnt

    def dataReceived(self, data):
        print 'line 13',data
        # self.transport.write('[%s] %s' % (ctime(), data))
    def dataSend(self,data):
        self.transport.write(data)

factory = protocol.Factory()
factory.protocol = TSServProtocol

print 'waiting for connection...'
if __name__ == '__main__':
    connect = reactor.listenTCP(PORT, factory)
    print '20'
    reactor.run()
    print '22'



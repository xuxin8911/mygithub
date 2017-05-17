#coding=utf-8
__author__ = 'xuxin'
from twisted.internet.protocol import Protocol, ClientFactory, ReconnectingClientFactory
from sys import stdout
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator
host = '192.168.5.217'
port = 8087
class Echo(Protocol):
    def connectionMade(self):
        # 连接上服务器后，打印出欢迎信息
        self.transport.write("Hello Server,I am the client\n")
    def sendMessage(self,msg):
        # 发送一条消息
        self.transport.write("MESSAGE:%s\n" % msg)

class EchoClientFactory(ReconnectingClientFactory):
	def startedConnecting(self, connector):
		print 'Started to connect.'

	def buildProtocol(self, addr):
		print 'Connected.'
		print 'Resetting reconnection delay'
		self.resetDelay()
		return Echo()

	def clientConnectionLost(self, connector, reason):
		print 'Lost connection. Reason:', reason
		ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

	def clientConnectionFailed(self, connector, reason):
		print 'Connection failed. Reason:', reason
		ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
#为使EchoClientFactory连接服务器，添加如下代码：
if __name__ == '__main__':
    c = ClientCreator(reactor,Echo)
    reactor.connectTCP(host, port, EchoClientFactory())
    reactor.run()
    print '34'
    # Echo = Echo()

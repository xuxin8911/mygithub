#coding:utf-8
from twisted.internet import protocol,reactor
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver
import re
import logging
import os
import sys
import ConfigParser
import time
logging.basicConfig(filename="agent.log",level=logging.DEBUG)

class AgentManageCommand(object):
    """
    与代理之间的通信命令格式
    """
    def __init__(self, action, **kw):
        self.action = action
        self.params = kw

    def toString(self):
#        self.compress()
        s = self.action
        ts = round(time.mktime(time.localtime()))
        self.params['ts'] = ts
        ps = ['%s="%s"' % (k, v) for k, v in self.params.items()]
        psr = ' '.join(ps)
        if psr:
            s += ' ' + psr
        return s + '\n'
		
    def compress(self):
        zparams = self.params.get(CommandParser.zparams, None)
        if zparams:
            zps = [p for p in zparams.split('|') if p]
            for zp in zps:
                zpv = self.params.get(zp, None)
                if zpv:
                    self.params[zp] = zlib.compress(zpv)
					
class AgentProtocol(LineReceiver):
    global agent_id,agent_name,agent_time_out
    agent_id = 0
    agent_name = "test"
    session_time_out = 10
    print agent_id
    def connectionMade(self):
    #连接成功，进行登录
        # global agent_id,agent_name
        cmd = AgentManageCommand("connect",id=agent_id,agent=agent_name)
        self.transport.write(cmd.toString())

    def lineReceived(self, line):
        print 'line 54'
        cmd = ""
        params={}
        print line
        logging.debug("接收到数据:%s" %line)
        tmpList = cmd.split(' ', line)
        action = tmpList[0].strip()
        params = tmpList[1]
        pat = '(\S+)="(\S*)"'
        kvs = re.findall(pat, params)
        params = {}
        params.update(kvs)
        try:
            if len(action) > 0:
                result = getattr(self, "action_"+action)(params)
                self.transport.write(result.toString())
        except:
			logging.warning("处理命令：%s异常："%cmd)

    def action_heartbeat(self):
        print 'line 73'
        cmd = AgentManageCommand("ping",id=agent_id,agent=agent_name)
        self.transport.write(cmd.toString())

    def action_connected(self,params):
        print 'line 78'
        self.agent_id = params.get('id', 0)
        reactor.callLater(self.heart_time, self.heartbeat)
    def action_listdir(self,params):
        print 'line 84'
        if not params.has_key("cur_dir"):
			return AgentManageCommand("ping",id=agent_id,agent=agent_name,error="参数错误")
        file = os.listdir(params["cur_dir"])
        #返回的file需要base64编码
        return AgentManageCommand("ping",id=agent_id,agent=agent_name,data=file)

class AgentClientFactory(ReconnectingClientFactory):
    def startedConnecting(self, connector):
        logging.debug("Started to connect.")

    def buildProtocol(self, addr):
        logging.debug('Connected:Resetting reconnection delay')
        self.resetDelay()
        return AgentProtocol()

    def clientConnectionLost(self, connector, reason):
        logging.warning('Lost connection.  Reason:%s'%reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        logging.warning('Connection failed.  Reason:%s'%reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector,reason)

host = '192.168.5.217'
port=8087
reactor.connectTCP(host, port, AgentClientFactory())
reactor.run()
			

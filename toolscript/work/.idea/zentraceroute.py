# coding=utf-8
__author__ = 'xuxin'

'''
链路检测功能：
1、实现链路检测功能，检测到异常切换路由器连接
2、每5秒遍历一次路由器虚Ip表，对每个虚IP发送10个ICMP ping命令，5个超时就生成一条事件
'''
import Globals
from twisted.internet import defer, reactor
from Products.ZenUtils.ZCmdBase import ZCmdBase
from Products.ZenHub.PBDaemon import FakeRemote, PBDaemon
from socket import gethostbyname, getfqdn, gaierror
from Products.Zuul.facades import ZuulFacade
import subprocess
import time
import socket
import struct
import threading
import traceback
import errno
import os
IPOPT_OPTVAL = 0
IPOPT_OLEN = 1
IPOPT_OFFSET = 2
IPOPT_RR = 8
IPOPT_MINOFF = 4
NROUTES =  9
standard_rate = 0.25   # 丢包率 > 75%链路不稳定

class ZenTraceroute(ZCmdBase):
    # name = agent = "zenping"
    icmp_list = []
    link_msg_list = []
    pinger = None
    def __init__(self):
        ZCmdBase.__init__(self)
        if not self.options.useFileDescriptor:
            self.openPrivilegedPort('--ping')

    def checksum(self,source_string):
        sum = 0
        countTo = (len(source_string)/2)*2
        count = 0
        while count<countTo:
            thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
            sum = sum + thisVal
            sum = sum & 0xffffffff
            count = count + 2
        if countTo<len(source_string):
            sum = sum + ord(source_string[len(source_string) - 1])
            sum = sum & 0xffffffff
        sum = (sum >> 16)  +  (sum & 0xffff)
        sum = sum + (sum >> 16)
        answer = ~sum
        answer = answer & 0xffff
        answer = answer >> 8 | (answer << 8 & 0xff00)
        return answer

    def get_head(self):
        packet = struct.pack("!BBHHH", 8, 0, 0, 0, 0)
        chksum=self.checksum(packet)
        packet = struct.pack("!BBHHH", 8, 0, chksum, 0, 0)

        head_len = 3 + 4*NROUTES + 1
        head = bytearray(head_len)
        head[0]=1
        head[1] = 7
        head[2]=39
        head[3]=8
        return packet,head

    def get_last_ip(self,buf,dest_name):
        a = ""
        def list_to_ip(ip_int):
            ip =  '.'.join((str(int(ip_int[0],16)),str(int(ip_int[1],16)),str(int(ip_int[2],16)),str(int(ip_int[3],16))))
            return ip
        for b in bytearray(buf):
            a = a+ "%x "%b
        buf_list = a.split(' ')
        list2 = []
        def hex_to_int(buf_list):
            for i in buf_list:
                if i:
                    list2.append(int(i,16))
            print list2
            self.log.info(str(list2))
        hex_to_int(buf_list)
        return 0
        if buf_list[21] == '27':
            start = 27
        elif buf_list[22] == '27':
            start = 28
        ip_list = []
        for n in xrange(0,8):
            ip_str = buf_list[start+n*4:start+(n+1)*4]
            ip =list_to_ip(ip_str)
            ip_list.append(ip)
            if ip == dest_name:
                break
        if len(ip_list) > 0:
            return ip_list[-1]
        else:
            return ''

    def get_real_ip(self,vip,ip1,ip2):   #通过traceroute获取虚IP对应的实际Ip
        # print 'vip = ',vip
        real_ip = ''
        dest_addr = socket.gethostbyname(vip)
        icmp = socket.getprotobyname('icmp')
        # send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = self.pingsocket
        packet,head = self.get_head()
        send_socket.setsockopt(socket.IPPROTO_IP,socket.IP_OPTIONS,str(head))
        send_socket.setblocking(1)
        send_socket.settimeout(2)
        try:
            send_socket.sendto(packet, (vip, 1))
            n = m = 0
            while True:
                try:
                    buf,addr =  send_socket.recvfrom(2048)
                    print 'vip = %s addr = %s ip1 = %s ip2 = %s n = %s m = %s\n'%(vip,str(addr),ip1,ip2,n,m)
                    if addr[0] == ip1 or addr[0] == ip2:
                        real_ip=addr[0]
                        break
                    print 'n = %s\n'%n
                    if n >  10:
                        real_ip = ''
                        break
                    n += 1
                except:
                    error = traceback.format_exc()
                    if 'timeout' in error or '[Errno 11]' in error:
                        if m > 10:
                            break
                        send_socket.sendto(packet, (vip, 1))
                        m += 1
                        n = 0
                        continue
                    else:
                        break
        except:
            # self.log.error('Exception = {0}'.format(Exception))
            self.log.error('{0} line 131 {1}'.format(vip,traceback.format_exc()))
        finally:
            # send_socket.close()
            m = n = 0
            return real_ip

    def get_link_msg(self,curs):
        '''
        获取虚IP列表
        :return:
        '''
        sql = '''select business1,ip_address1,station_address1,business2,ip_address2,station_address2,vip,traceroute_status,id from net_link_check'''
        curs.execute(sql)
        result = curs.fetchall()
        link_msg_list = []
        for i in result:
            link_msg_dict = dict(business1 = i[0],ip_address1 = i[1],station_address1 = i[2],business2 = i[3],ip_address2 = i[4],
                                 station_address2 = i[5],vip = i[6],traceroute = i[7],id = i[8])
            link_msg_list.append(link_msg_dict)
        return link_msg_list

    def update_link_sql(self,curs):
        '''
        根据traceroute结果，更新链路检测表状态
        :return:
        '''
        def update_data(vip,status):
            sql = "update net_link_check set traceroute_status = '{0}' where vip = '{1}'".format(status,vip)
            curs.execute(sql)
        for link_msg in self.link_msg_list:
            for i in self.icmp_list:
                if i['vip'] == link_msg['vip']:
                    if i['count'] !=0:
                        rate = float(i['success'])/float(i['count'])
                    else:
                        rate = 0
                    if i['real_ip'] == '':
                        status = 0    #网络不可达
                    elif i['real_ip'] == '#':
                        status = 3          #网络正在切换中
                    elif i['real_ip'] == link_msg['ip_address1']:
                        status = 1         #网络1可达
                        if rate < standard_rate:
                            status = 0
                    elif i['real_ip'] == link_msg['ip_address2']:
                        status = 2          #网络2可达
                        if rate < standard_rate:
                            status = 0
                    update_data(i['vip'],status)
        self.icmp_list = []

    def get_cmd_real(self,vip):
        cmd = 'traceroute %s -m 8 -w 3'%vip  #最多接收8个，超时3秒
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        ret1 =  p.stdout.readlines()
        print ret1
        try:
            last_ret = ret1[-1]
            real_ip = str(last_ret.split(None)[2]).replace('(','').replace(')','')
            if len(real_ip.split('.')) != 4:  #不是
                real_ip = ''
        except:
            real_ip = ''
        return real_ip

    def update_link(self,vip,ip1,ip2):
        real_ip = ''
        # self.log.info('start get real_ip...')
        try:
            # real_ip = self.get_real_ip(vip,ip1,ip2)
            real_ip = self.get_cmd_real(vip)
            print 'vip = %s,real_ip = %s\n'%(vip,real_ip)
            # time.sleep(1)
        except:
            self.log.error('line 196 %s',traceback.format_exc())
        # self.log.info('end get_real_ip...')
        flag = 0
        for i in self.icmp_list:
            if i['vip'] == vip:
                flag = 1
                if real_ip:
                    if i['real_ip'] == real_ip:
                        i['count'] += 1
                        i['success'] += 1
                    else:
                        if i['real_ip'] == '':
                            i['real_ip'] == real_ip
                        elif i['real_ip'] == '#':  #    *代表前后获取的实际IP不一致
                            pass
                        else:
                            i['real_ip'] == '#'
                else:
                    i['count'] += 1
        if not flag:
            if real_ip:
                self.icmp_list.append(dict(vip=vip,real_ip=real_ip,count=1,success=1))
            else:
                self.icmp_list.append(dict(vip=vip,real_ip='',count=1,success=0))

    def buildOptions(self):
        ZCmdBase.buildOptions(self)
        self.parser.add_option('--name',
                               dest='name',
                               default=getfqdn(),
                               help=("host that roots the ping dependency "
                                     "tree: typically the collecting hosts' "
                                     "name; defaults to our fully qualified "
                                     "domain name (%s)" % getfqdn()))
        self.parser.add_option('--test',
                               dest='test',
                               default=False,
                               action="store_true",
                               help="Run in test mode: doesn't really ping,"
                               " but reads the list of IP Addresses that "
                               " are up from /tmp/testping")
        self.parser.add_option('--useFileDescriptor',
                               dest='useFileDescriptor',
                               default=None,
                               help=
                               "use the given (privileged) file descriptor")
        self.parser.add_option('--minConfigWait',
                               dest='minconfigwait',
                               default=300,
                               type='int',
                               help=
                               "the minimal time, in seconds, "
                               "between refreshes of the config")
    def getPinger(self):
        # from pydev import pydevd
        # pydevd.settrace('192.168.1.153',port=7000,stdoutToServer=True,stderrToServer=True)
        if self.pinger:
            self.pinger.reconfigure(self.pingTries, self.pingTimeOut)
        else:
            fd = None
            if self.options.useFileDescriptor is not None:
                fd = int(self.options.useFileDescriptor)
            self.createPingSocket(fd)

    def createPingSocket(self, sock):
        """make an ICMP socket to use for sending and receiving pings"""
        socketargs = socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP
        if sock is None:
            try:
                s = socket
                self.pingsocket = s.socket(*socketargs)
            except socket.error, e:
                err, msg = e.args
                if err == errno.EACCES:
                    self.log.error("must be root to send icmp.")
                raise e
        else:
            self.pingsocket = socket.fromfd(sock, *socketargs)
            os.close(sock)
        # self.pingsocket.setblocking(0)
        # reactor.addReader(self)

    def run(self):
        '''
        主函数，定时发送traceroute命令
        :return:
        '''
        # from pydev import pydevd
        # pydevd.settrace('192.168.1.153',port=7000,stdoutToServer=True,stderrToServer=True)
        # self.log.info('start zentraceroute...')
        # vip = '198.4.33.10'
        # # vip = '198.8.0.10'
        # self.get_cmd_real(vip)
        # return
        try:
            # self.getPinger()
            # host = '198.3.21.10'
            # host = '198.6.8.10'
            # ip1 = '168.168.11.2'
            # ip2 = '168.168.3.2'
            # t1 = time.time()
            # real_ip = self.get_real_ip(host,ip1,ip2)   #链路检测获取链路测试
            # print time.time() - t1
            # print 'real_ip = ',real_ip
            # return 0
            dbpool = self.dmd._getOb('ZenSSOCDBSpool')
            # get_mysql = GetMysql()
            # dbpool = get_mysql.get_dbpool()
            conn = dbpool.connect()
            curs = conn.cursor()
            self.link_msg_list = self.get_link_msg(curs)
            t1 = time.time()
            while True:
                t2 = time.time()
                for i in xrange(0,12):
                    t3 = time.time()
                    a = 0
                    for link_msg in self.link_msg_list:
                        vip,ip1,ip2 = link_msg['vip'],link_msg['ip_address1'],link_msg['ip_address2']
                        # print '---------   ',vip,ip1,ip2,'  ---------\n'
                        t = threading.Thread(target=self.update_link,args=(vip,ip1,ip2))
                        t.start()
                        # ip1 = '168.168.1.2'
                        # ip2 = '168.168.3.2'
                        # if link_msg['vip'] == '198.6.8.10':
                        #     vip = '198.6.8.10'
                        #     self.update_link(vip,ip1,ip2)
                        # self.update_link_status(link_msg['vip'],curs)
                    self.log.info( '----------------------------  {0}   --------------- {1}'.format(i,time.time()-t3))
                    time.sleep(5)  #5s检查一次
                    break
                # self.log.error(self.icmp_list)
                self.update_link_sql(curs)
                time.sleep(5)   #检测完一轮暂停5s
                self.log.error('完成一轮检测时间：{0}'.format(time.time()-t2))
            dbpool.close(conn)
        except:
            self.log.error('line 332 %s'%traceback.format_exc())
        finally:
            if self.pingsocket:
                # reactor.removeReader(self)
                self.pingsocket.close()

# class GetMysql(ZCmdBase):
#     def __init__(self):
#         ZCmdBase.__init__(self)
#
#     def get_dbpool(self):
#         return self.dmd._getOb('ZenSSOCDBSpool')

if __name__ == '__main__':
    # from pydev import pydevd
    # pydevd.settrace('192.168.1.153',port=7000,stdoutToServer=True,stderrToServer=True)
    Traceroute = ZenTraceroute()
    Traceroute.run()
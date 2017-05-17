# coding=utf-8
__author__ = 'xuxin'

'''
链路检测功能：
1、实现链路检测功能，检测到异常切换路由器连接
2、每5秒遍历一次路由器虚Ip表，对每个虚IP发送10个ICMP ping命令，5个超时就生成一条事件
'''
# import Globals
# from twisted.internet import defer, reactor
# from Products.ZenUtils.ZCmdBase import ZCmdBase
import subprocess
import time
import socket
import struct
import threading
IPOPT_OPTVAL = 0
IPOPT_OLEN = 1
IPOPT_OFFSET = 2
IPOPT_RR = 7
IPOPT_MINOFF = 4
NROUTES =  9
standard_rate = 0.25   # 丢包率 > 75%链路不稳定

class ZenTraceroute():
    name = agent = "zenping"
    icmp_list = []
    link_msg_list = []
    def __init__(self):
        # ZCmdBase.__init__(self)
        pass

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

    def get_last_ip(self,buf):
        a = ""
        def int_to_ip(ip_int):
            ip =  '.'.join((str(int(ip_int[0],16)),str(int(ip_int[1],16)),str(int(ip_int[2],16)),str(int(ip_int[3],16))))
            return ip
        for b in bytearray(buf):
            a = a+ "%x "%b
        buf_list = a.split(' ')
        if buf_list[21] == '27':
            start = 27
        elif buf_list[22] == '27':
            start = 28
        buf_list = a.split(' ')
        ip_list = []
        for n in xrange(0,9):
            ip = buf_list[start+n*4:start+(n+1)*4]
            ip_list.append(int_to_ip(ip))
        return ip_list[-1]   #返回traceroute链路最后一个IP地址

    def get_real_ip(self,dest_name):   #通过traceroute获取虚IP对应的实际Ip
        dest_addr = socket.gethostbyname(dest_name)
        icmp = socket.getprotobyname('icmp')
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        packet,head = self.get_head()
        send_socket.setsockopt(socket.IPPROTO_IP,socket.IP_OPTIONS,str(head))
        send_socket.setblocking(0)
        send_socket.settimeout(1)
        send_socket.sendto(packet, (dest_name, 1))
        real_ip = ''
        try:
            n = 0
            while True:
                n += 1
                buf,addr =  send_socket.recvfrom(2048)
                if addr[0] == dest_name:
                    real_ip = self.get_last_ip(buf)
                    # self.update_link_sql(dest_name,real_ip,curs)
                    # return real_ip,True
                    break
                if n > 5:
                    break
        except socket.error:
            pass
        finally:
            send_socket.close()

            return real_ip

    def __get_link_msg(self,curs):
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
            print 'sql = ',sql
            curs.execute(sql)
        for link_msg in self.link_msg_list:
            for i in self.icmp_list:
                if i['vip'] == link_msg['vip']:
                    print i
                    if i['count'] !=0:
                        rate = float(i['success'])/float(i['count'])
                    else:
                        rate = 0
                    print rate
                    if i['real_ip'] == '':
                        status = 0    #网络不可达
                    elif i['real_ip'] == '*':
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

    def update_link(self):
        vip = '192.168.1.155'
        real_ip = self.get_real_ip(vip)
        print vip,real_ip
        return
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
                        elif i['real_ip'] == '*':  #    *代表前后获取的实际IP不一致
                            pass
                        else:
                            i['real_ip'] == '*'
                else:
                    i['count'] += 1
        if not flag:
            if real_ip:
                self.icmp_list.append(dict(vip=vip,real_ip=real_ip,count=1,success=1))
            else:
                self.icmp_list.append(dict(vip=vip,real_ip='',count=1,success=0))

    def run(self):
        '''
        主函数，定时发送traceroute命令
        :return:
        '''
        # vip_list = ['192.168.1.155','192.168.1.167','192.168.1.153']
        # from pydev import pydevd
        # pydevd.settrace('192.168.1.153',port=7000,stdoutToServer=True,stderrToServer=True)
        real_ip = self.get_real_ip('192.168.1.155')
        # return
        # dbpool = self.dmd._getOb('ZenSSOCDBSpool')
        # conn = dbpool.connect()
        # curs = conn.cursor()
        # self.link_msg_list = self.get_link_msg(curs)
        self.link_msg_list = [{'vip':'192.168.1.155'}]
        t1 = time.time()
        print len(self.link_msg_list)
        while True:
            t2 = time.time()
            for i in xrange(0,12):
                t3 = time.time()
                for link_msg in self.link_msg_list:
                    t = threading.Thread(target=self.update_link)
                    t.start()
                    # self.update_link_status(link_msg['vip'],curs)
                print '----------------------------  ',i,'   ---------------',time.time()-t3
                time.sleep(5)
            print self.icmp_list
            # self.update_link_sql(curs)
            print '完成一轮检测时间：',time.time()-t2
        # dbpool.close(conn)

if __name__ == '__main__':
    # from pydev import pydevd
    # pydevd.settrace('192.168.1.153',port=7000,stdoutToServer=True,stderrToServer=True)
    Traceroute = ZenTraceroute()
    Traceroute.run()
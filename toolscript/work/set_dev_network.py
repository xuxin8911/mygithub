#!/usr/bin/python
#conding = utf-8
__author__ = 'Administrator'
import subprocess
from Products.ZenUtils.ZenScriptBase import ZenScriptBase

#控制文件保护的运行或停止
class ActionCmd(ZenScriptBase):
    def control_file_protect(self,enabled,dest_ip):
        self.connect()
        dbpool = self.dmd._getOb('ZenSSOCDBSpool')
        conn = dbpool.connect()
    def get_nmap_info(self):
        cmd = 'nmap -sP 192.168.1.0/24'
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
        ret1 = p.stdout.readlines()
        ret1 = ['\n', 'Starting Nmap 5.51 ( http://nmap.org ) at 2014-08-18 17:40 CST\n',
                'Failed to find device eth4 which was referenced in /proc/net/route\n',
                'Failed to find device eth6 which was referenced in /proc/net/route\n',
                'Failed to find device br-svc which was referenced in /proc/net/route\n',
                'Failed to find device br-adm which was referenced in /proc/net/route\n',
                'Nmap scan report for 192.168.1.1\n', 'Host is up (0.00034s latency).\n','MAC Address: 70:9B:A5:01:96:0D (Unknown)\n',
                'Nmap scan report for 192.168.1.13\n','Host is up (0.00093s latency).\n', 'MAC Address: 52:54:00:D8:B7:AC (QEMU Virtual NIC)\n',
                'Nmap scan report for 192.168.1.14\n', 'Host is up (0.00073s latency).\n','MAC Address: 52:54:00:4C:0A:02 (QEMU Virtual NIC)\n',
                'Nmap scan report for 192.168.1.15\n', 'Host is up (0.00030s latency).\n', 'MAC Address: 00:1E:08:09:81:00 (Centec Networks)\n',
                'Nmap scan report for 192.168.1.103\n', 'Host is up (0.0056s latency).\n', 'MAC Address: 34:40:B5:D5:C6:D2 (Unknown)\n',
                'Nmap scan report for 192.168.1.104\n', 'Host is up (0.00024s latency).\n', 'MAC Address: 00:1F:D0:89:78:5F (Giga-byte Technology Co.)\n',
                'Nmap scan report for 192.168.1.105\n', 'Host is up (0.00055s latency).\n', 'MAC Address: 52:54:00:FF:F4:6A (QEMU Virtual NIC)\n',
                'Nmap scan report for 192.168.1.254\n', 'Host is up (0.00074s latency).\n', 'MAC Address: 70:9B:A5:10:00:72 (Unknown)\n', 'Nmap done: 256 IP addresses (92 hosts up) scanned in 134.42 seconds\n']
        print ret1
        n = 0
        ip_mac_list = []
        for i in xrange(len(ret1)):
            str2 = '123'
            if ret1[i].startswith('Nmap scan report for'):
                ip = ret1[i][21:len(ret1[i])-1]
                mac = ret1[i+2][13:30]
                ip_mac_list.append(dict(ip = ip,mac = mac))
        print ip_mac_list
if __name__ == '__main__':
    get_nmap_info()
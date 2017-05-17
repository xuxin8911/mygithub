# coding=utf-8
__author__ = 'xuxin'
'''
功能：判断ip地址对应的端口是否有监听

配置文件:ipaddr.cfg
[config]
#ip用双引号，IP段中间用"-"隔开
ip_list = ["222.35.13.162-222.35.13.180","114.247.150.1-114.247.150.20","192.168.1.166"]
#端口为int型
port_list = [4483,4583,4683,4783]
#超时时间
timeout = 3
#轮询时间
polling_time = 60
'''

import socket
import threading
import time
import traceback
import logging
import ConfigParser
import json
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='check.log',
                    filemode='a')

def read_config():
    config = ConfigParser.ConfigParser()
    path = 'ipaddr.cfg'
    ret_ip_list = []
    port_list = []
    try:
        config.read(path)
        ip_list = json.loads(config.get('config','ip_list'))
        port_list = json.loads(config.get('config','port_list'))
        timeout = json.loads(config.get('config','timeout'))
        polling_time = json.loads(config.get('config','polling_time'))
        for ip in ip_list:
            if '-' in ip:
                ip_int1 = int(ip.split('-')[0].split('.')[-1])
                ip_int2 = int(ip.split('-')[1].split('.')[-1])
                for i in range(ip_int1,ip_int2):
                    ret_ip_list.append('.'.join((ip.split('-')[0].split('.')[0],ip.split('-')[0].split('.')[1],ip.split('-')[0].split('.')[2],str(i))))
                ret_ip_list.append(ip.split('-')[1])
            else:
                ret_ip_list.append(ip)
    except:
        logging.error(traceback.format_exc())
    finally:
        return dict(ip_list=ret_ip_list,port_list=port_list,timeout=timeout,polling_time=polling_time)

def check_listen(ip,port,timeout):
    try:
        t_start = time.time()
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.settimeout(timeout)
        client.connect((ip,port))
        t_end = time.time()
        logging.info('Server {0}:{1} is listen use {2}s\n'.format(ip,port,t_end-t_start))
    except Exception:
        logging.error('Server {0}:{1} is not listen\n'.format(ip,port))
    finally:
        client.close()

if __name__ == '__main__':
    server_dict = read_config()
    ip_list = server_dict.get('ip_list',[])
    port_list = server_dict.get('port_list',[])
    timeout = server_dict.get('timeout',1)
    polling_time = server_dict.get('polling_time',5)
    while True:
        for ip in ip_list:
            for port in port_list:
                t = threading.Thread(target=check_listen,args=(ip,port,timeout))
                t.setDaemon(True)
                t.start()
        time.sleep(polling_time)
        logging.info('---------------------------------------------------------------')

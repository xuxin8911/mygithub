# coding=utf-8
__author__ = 'xuxin'

'''
民生web检测与业务恢复，最终版
'''
import httplib
import os
import socket
import subprocess
import logging
import time
import traceback
import requests
import threading

CYCLE_TIME = 60  # 志愿者应用8088启动需要65秒，最多到75秒，将检测循环时间设置大些，设置90秒，一般设置30秒
START_TIME = 5
TIME_OUT = 15

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='http_check.log',
                    filemode='a')
#注:host为127.0.0.1 or 域名(有的web配置的域名才能访问)
http_info_list = [dict(address = '127.0.0.1',http_port=80,http_url='',exec_dir='D:\\apache-tomcat-6.0.36\\bin\\startup.bat')]

def http_check(address,http_port, startup_dir, http_url='', web_type=0):
    def get_requests(address,http_port, http_url):
        try:
            status = 1
            url = 'http://{0}:{1}{2}'.format(address,str(http_port), http_url)
            logging.info(url)
            host = '{0}:{1}'.format(address,str(http_port))
            r1 = requests.get(url, headers={"Host": host,
                                            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
                                            "Accept": "text/plain"}, timeout=(TIME_OUT, TIME_OUT))
            status = r1.status_code
            r1.close()
        except socket.error, msg:
            logging.error('socket error:%s', msg)
            status = -1
        except Exception,e:
            logging.error(e.message)
        finally:
            return status

    status = get_requests(address,http_port, http_url)
    if status not in [200, 302, 301]:
        logging.error('http_port {0} status = {1}'.format(http_port, status))
        http_recover(http_port, startup_dir, web_type=0)
    else:
        cmd1 = 'netstat -aon |find "0.0.0.0:{0}"'.format(http_port)
        context1 = os.popen(cmd1).read()
        if context1:
            # logging.info("Web Application {0} Status OK:{1}......".format(http_port,status))  #状态OK不打印日志
            pass
        else:
            logging.error('http_port {0} status = {1}'.format(http_port, status))
            http_recover(http_port, startup_dir, web_type=0)


def http_recover(http_port, startup_dir, web_type=0):
    '''
    :param http_port:
    :param startup_dir:
    :param web_type:0:Tomcat  1:Apache，默认为0
    :return:
    '''

    def get_pid():
        cmd1 = 'netstat -aon |find "0.0.0.0:{0}"'.format(http_port)
        context1 = os.popen(cmd1).read()
        if context1:
            pid = context1.split()[4]
            return pid
        else:
            return ''

    pid = get_pid()
    num = 0
    while pid:
        if num > 3:
            break
        cmd2 = 'taskkill /f /pid {0}'.format(pid)
        context2 = os.popen(cmd2).read()
        logging.info("kill http port:%s" % http_port)
        time.sleep(START_TIME)
        pid = get_pid()
        num += 1

    '''
    cmd3 = 'netstat -ano |find "{0}"'.format(http_port)
    for i in range(60):   #如果端口占用，休眠一秒，如果检查30次依然占用，继续后续操作
        context3 = os.popen(cmd3).read()
        if context3:
            time.sleep(1)
            continue
        break
    '''

    if web_type == 0:
        startup_base = '\\'.join(startup_dir.split('\\')[:-1])
        os.chdir(startup_base)
        subprocess.Popen(startup_dir)
    elif web_type == 1:
        cmd1 = 'net stop Apache2.2'
        cmd2 = 'net start Apache2.2'
        os.system(cmd1)
        os.system(cmd2)
        # logging.info("restart web application {0}".format(http_port))


def run():
    logging.info('start check web...')
    while True:
        try:
            threads = []
            for i in http_info_list:
                host = i.get('address','127.0.0.1')
                http_port = i.get('http_port','')
                if not http_port:
                    continue
                t1 = threading.Thread(target=http_check, args=(host,i['http_port'], i['exec_dir'], i['http_url']))
                threads.append(t1)
            for t in threads:
                t.start()
                time.sleep(0.5)  # 每个应用启动间隔0.5秒

        except:
            logging.error(traceback.format_exc())
        time.sleep(CYCLE_TIME)
        logging.info('check web end!\n')


if __name__ == '__main__':
    run()


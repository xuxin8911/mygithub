# coding=utf-8
__author__ = 'xuxin'
'''
非正常结束weblogic启动
1、通过requests判断页面是否正常
2、如果页面异常，先kill对应的进程
3、然后rm lok文件和DAT文件
4、启动对应的进程
'''
import os
import subprocess
import requests
import socket
import logging

DOMAIN_HOME = '/weblogic/Oracle/Middleware/user_projects/domains/base_domain'

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m%d %H:%M:%S',
                    filename='weblogic_check.log',
                    filemode='w')

def http_check(http_port,startup_dir,http_url='',web_type=0):
    def get_requests(http_port,http_url):
        try:
            status = 1
            url = ''.join(('http://127.0.0.1:',str(http_port),http_url))
            host = ''.join(('127.0.0.1:',str(http_port)))
            r1 = requests.get(url,headers={"Host": host,"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5","Accept": "text/plain"},timeout=(5,5))
            status = r1.status_code
            r1.close()
        except socket.error,msg:
            logging.info('socket error:%s',msg)
            status = -1
        finally:
            return status

    status = get_requests(http_port,http_url)
    if status not in [200,302,301]:
        logging.error('http_port {0} status = {1}'.format(http_port,status))
        http_recover(http_port,startup_dir,web_type=0)
    else:
        cmd1 = 'netstat -aon |find "0.0.0.0:{0}"'.format(http_port)
        context1 = os.popen(cmd1).read()
        if context1:
            #logging.info("Web Application {0} Status OK:{1}......".format(http_port,status))  #状态OK不打印日志
            pass
        else:
            logging.error('http_port {0} status = {1}'.format(http_port,status))
            http_recover(http_port,startup_dir,web_type=0)

def kill_pid(http_port):
    '''
    kill 端口多占用的进程
    :param http_port:
    :return:
    '''
    cmd1 = 'netstat -aon |find "0.0.0.0:{0}"'.format(http_port)
    context1 = os.popen(cmd1).read()
    if context1:
        pid = context1.split()[4]
        cmd2 = 'kill -9 {0}'.format(pid)
        context2 = os.popen(cmd2).read()
        logging.info("kill http port:%s"%http_port)
    return True

def remove_file():
    '''
    删除domain_home目录下面的*.lok文件
    :param domain_home:
    :return:
    '''
    def rm_lok(lok_file):
        if os.path.exists(lok_file):
            cmd = 'rm -f {0}'.format(lok_file)
            p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
            ret = p.stdout.read()

    def rm_DAT():
        find_cmd = 'find servers -name "*.DAT"'
        find_p = subprocess.Popen(find_cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
        find_ret = find_p.stdout.readlines()
        for DAT in find_ret:
            cmd = 'rm -f {0}'.format(DAT)
            p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
            ret = p.stdout.read()

    lok_file1 = 'edit.lok'
    lok_file2 = 'config/config.lok'
    lok_file3 = 'servers/AdminServer/tmp/AdminServer.lok'
    lok_file4 = 'servers/AdminServer/data/ldap/ldapfiles/EmbeddedLDAP.lok'
    rm_lok(lok_file1)
    rm_lok(lok_file2)
    rm_lok(lok_file3)
    rm_lok(lok_file4)
    rm_DAT()
    return True

def http_recover(start_dir):
    kill_pid()
    remove_file()
    cmd = "nohup sh {0} &".format(start_path)
    os.system(cmd)

if __name__ == '__main__':
    os.chdir(DOMAIN_HOME)
    http_port = 80
    http_url = '/culture/FreeTicketAction_freeTicketHome.do?activeG=all'
    start_path = '/bin/startWebLogic.sh'
    http_check(http_port,start_path,http_url)

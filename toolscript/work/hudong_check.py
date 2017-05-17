# coding=utf-8
__author__ = 'xuxin'

'''
东城互动调查web检测与业务恢复，最终版
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

CYCLE_TIME = 90   #志愿者应用8088启动需要65秒，最多到75秒，将检测循环时间设置大些，设置90秒
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='hudong_check.log',
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

def http_recover(http_port,startup_dir,web_type=0):
    '''
    :param http_port:
    :param startup_dir:
    :param web_type:0:Tomcat  1:Apache，默认为0
    :return:
    '''
    cmd1 = 'netstat -aon |find "0.0.0.0:{0}"'.format(http_port)
    context1 = os.popen(cmd1).read()
    if context1:
        pid = context1.split()[4]
        cmd2 = 'taskkill /f /pid {0}'.format(pid)
        context2 = os.popen(cmd2).read()
        logging.info("kill http port:%s"%http_port)
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
    logging.info("restart web application {0}".format(http_port))

if __name__ == '__main__':
    while True:
        try:
            logging.info('start check hudong web...' )
            threads = []
            #1、政民互动
            zhengminhudong_port = 9080
            zhengminhudong_url = '/manage'
            zhengminhudong_dir = 'E:\\tomcat-6.0.16-jdk6zmhd\\bin\\startup.bat'
            t1 = threading.Thread(target=http_check,args=(zhengminhudong_port,zhengminhudong_dir,zhengminhudong_url))
            threads.append(t1)
            
            #2、办事查询
            banshichaxun_port = 8050
            banshichaxun_url = '/synDatas/asop/lists'
            banshichaxun_dir = 'E:\\tomcat-5.5.26-chaxun\\bin\\startup.bat'
            t2 = threading.Thread(target=http_check,args=(banshichaxun_port,banshichaxun_dir,banshichaxun_url))
            threads.append(t2)

            #3、直播后台
            zhibohoutai_port = 8090
            zhibohoutai_url = '/direct/displayLogin.do'
            zhibohoutai_dir = 'E:\\asop-tomcatziht\\asop-tomcat\\bin\\startup.bat'
            t3 = threading.Thread(target=http_check,args=(zhibohoutai_port,zhibohoutai_dir,zhibohoutai_url))
            threads.append(t3)
            
            #4、直播前台
            zhiboqiantai_port = 8081
            zhiboqiantai_url = '/asop'
            zhiboqiantai_dir = 'E:\\tomcat-zhibo-8081\\bin\\startup.bat'
            t4 = threading.Thread(target=http_check,args=(zhiboqiantai_port,zhiboqiantai_dir,zhiboqiantai_url))
            threads.append(t4)
            #5、访谈后台
            fangtanhoutai_port = 6666
            fangtanhoutai_url = '/fangtanguanli/login.do'
            fangtanhoutai_dir = 'E:\\asop-jiv-new\\bin\\startup.bat'
            t5 = threading.Thread(target=http_check,args=(fangtanhoutai_port,fangtanhoutai_dir,fangtanhoutai_url))
            threads.append(t5)
            #6、访谈前台
            fangtanqiantai_port = 8083
            fangtanqiantai_url = '/fangtan'
            fangtanqiantai_dir = 'E:\\asop-jivnew\\bin\\startup.bat'
            t6 = threading.Thread(target=http_check,args=(fangtanqiantai_port,fangtanqiantai_dir,fangtanqiantai_url))
            threads.append(t6)
            #7、调查
            diaocha_port = 8084
            diaocha_url = '/papernew/admin/login.jsp'
            diaocha_dir = 'E:\\tomcat-5.5.26-diaocha\\bin\\startup.bat'
            t7 = threading.Thread(target=http_check,args=(diaocha_port,diaocha_dir,diaocha_url))
            threads.append(t7)
            #8、志愿者网站
            # zhiyuanzheweb_port = 80
            # zhiyuanzheweb_dir = ''
            # web_type = '1'
            # http_check(zhiyuanzheweb_port,zhiyuanzheweb_dir,web_type)

            #9、志愿者应用
            zhiyuanzheapp_port = 8088
            zhiyuanzheapp_url = '/volunteer/portal/login.jsp'
            zhiyuanzheapp_dir = 'E:\\tomcat-zhiyuanzhe-8088\\tomcat-zhiyuanzhe-8088\\bin\\startup.bat'
            t9 = threading.Thread(target=http_check,args=(zhiyuanzheapp_port,zhiyuanzheapp_dir,zhiyuanzheapp_url))
            threads.append(t9)
            
            #10、留言板
            liuyanban_port = 8082
            liuyanban_url = '/jdzxlyb/index_bm.jsp?bm=1'
            liuyanban_dir = 'E:\\jakarta-tomcat-5.0.28\\bin\\startup.bat'
            t10 = threading.Thread(target=http_check,args=(liuyanban_port,liuyanban_dir,liuyanban_url))
            threads.append(t10)
            #11、在线答题  暂时未迁
            # zaixiandati_port = 8080
            # zaixiandati_url = ''
            # zaixiandati_dir = ''

            #12、志愿者后台管理  没看到
            zhiyuanzhehoutai_port = 8089
            zhiyuanzhehoutai_url = '/manageweb/login.jsp'
            zhiyuanzhehoutai_dir = 'E:\\tomcat-zhiyuanzhe-wangzhan-8089\\tomcat-zhiyuanzhe-wangzhan-8089\\bin\\startup.bat'
            t12 = threading.Thread(target=http_check,args=(zhiyuanzhehoutai_port,zhiyuanzhehoutai_dir,zhiyuanzhehoutai_url))
            threads.append(t12)

            for t in threads:
                t.start()
                time.sleep(0.5) #每个应用启动间隔0.5秒
            logging.info('check hudong web end!\n')
        except:
            logging.error(traceback.format_exc())
        time.sleep(CYCLE_TIME)

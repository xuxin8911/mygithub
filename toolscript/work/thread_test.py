#coding=utf-8
__author__ = 'xuxin'

import telnetlib
import time
import traceback
import thread
import threading
def ping_status(ip1,iplist):
    user='admin'
    passwd = '123456'
    # command = 'ping %s'%ip2
    flag = False
    tn = None
    try:
        try:
            tn = telnetlib.Telnet(host=ip1,timeout=1)
        except:
            print 'cannot open host'
            return flag
        tn.read_until('Password: ',0.5)
        tn.write(passwd+'\n')
        #判断登陆是否成功
        login = tn.read_until(b"Microsoft Telnet Server",0.5)
        if "Incorrect Password!" in login:
            print 'Incorrect Password!'
            return flag
        statusList = []
        threads = []
        for i in iplist:
            print i
            t= threading.Thread(target=worker,args=(tn,i))
            threads.append(t)
            t.start()
            # t.join()
        # for i in xrange(len(iplist)):
        #     threads[i].start()
        # for i in xrange(len(iplist)):
        #     threads[i].join()
            # statusList.append(status_dict)
        print statusList
    except:
        print traceback.format_exc()
        flag = False
    finally:
        if tn:
            tn.close()
            del tn

def worker(tn,ip):
    # print ip,'------------------'
    flag = 'Up'
    status_dict = {}
    status_dict[ip] = flag
    print 'line 46--------------------\n'
    print status_dict
    print 'line 48-------------------'
    # thread.exit_thread()

if __name__ == '__main__':
    ip1 = '192.168.60.15'
    iplist = ['192.168.60.125','192.168.60.15']
    t1 = time.time()
    status = ping_status(ip1,iplist)
    # status = ping_status2(ip1,ip2)
    t2 = time.time() - t1
    print t2

#coding=utf-8
__author__ = 'xuxin'

import telnetlib
import time
import traceback
import thread
import threading
import pexpect

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
        # tn.read_until('login: ',0.5)
        # tn.write(user + '\n')
        tn.read_until('Password: ',0.5)
        tn.write(passwd+'\n')
        #判断登陆是否成功
        login = tn.read_until(b"Microsoft Telnet Server",0.5)
        if "Incorrect Password!" in login:
            print 'Incorrect Password!'
            return flag
        statusList = []
        for i in iplist:
            print i
            # threads = []
            # t= threading.Thread(target=worker,args=(tn,i))
            # threads.append(t)
            # t.start()
            # # for i in threads:
            # #     i.start()
            # # for i in threads:
            # #     i.join()
            status = worker(tn,i)
            print 'line 42 ',status
        print statusList
    except:
        print traceback.format_exc()
        flag = False
    finally:
        if tn:
            tn.close()
            del tn

def worker2(tn,ip):
    print ip
    print '\nline 65\n'

def worker(tn,ip):
    # print ip,'------------------'
    print 'line 62'
    command = 'ping -c 3 %s\n'%ip
    # command = 'ping -c 3 192.168.1.155\n'
    timeout = 3
    msg = tn.read_until('$')
    tn.write(command)
    msg = tn.read_until('\n')
    # tn.write('exit\n')
    tmp = tn.read_very_eager()
    str1 = 'packet loss'
    time1 = time.time()
    print tmp
    while(tmp.find(str1) < 0):
        time2 = time.time() - time1
        print time2
        # if time2 > 6:
        #     break
        # else:
        time.sleep(1)
        print 'wait....'
        tmp = tn.read_very_eager()
    print tmp
    print '-----------',time.time() - time1
    str2 = "100.0 % packet loss"
    if tmp.find(str1) > 0:
        if tmp.find(str2) > 0:
            flag = 'Down'
        else:
            flag = 'Up'
    else:
        flag = 'Down'
    status_dict = {}
    status_dict[ip] = flag
    return flag

def pexpect_telnet():
    # 拼凑 telnet 命令
    ipAddress = '192.168.60.15'
    loginName = 'root'
    loginPassword = '123456'
    loginprompt = '[$#>]'
    cmd = 'telnet ' + ipAddress
    # 为 telnet 生成 spawn 类子程序
    child = pexpect.spawn(cmd)
    # 期待'login'字符串出现，从而接下来可以输入用户名
    index = child.expect(["login", "(?i)Unknown host", pexpect.EOF, pexpect.TIMEOUT])
    if ( index == 0 ):
        # 匹配'login'字符串成功，输入用户名.
        child.sendline(loginName)
        # 期待 "[pP]assword" 出现.
        index = child.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT])
        # 匹配 "[pP]assword" 字符串成功，输入密码.
        child.sendline(loginPassword)
        # 期待提示符出现.
        child.expect(loginprompt)
        if (index == 0):
            # 匹配提示符成功，输入执行命令 'ls -l'
            child.sendline('ls -l')
            # 立马匹配 'ls -l'，目的是为了清除刚刚被 echo 回显的命令.
            child.expect('ls -l')
            # 期待提示符出现.
            child.expect(loginprompt)
            # 将 'ls -l' 的命令结果输出.
            print child.before
            print "Script recording started. Type ^] (ASCII 29) to escape from the script  shell."
            # 将 telnet 子程序的执行权交给用户.
            child.interact()
            print 'Left interactve mode.'
        else:
            # 匹配到了 pexpect.EOF 或 pexpect.TIMEOUT，表示超时或者 EOF，程序打印提示信息并退出.
            print "telnet login failed, due to TIMEOUT or EOF"
            child.close(force=True)
    else:
        # 匹配到了 pexpect.EOF 或 pexpect.TIMEOUT，表示超时或者 EOF，程序打印提示信息并退出.
        print "telnet login failed, due to TIMEOUT or EOF"
        child.close(force=True)

if __name__ == '__main__':
    ip1 = '192.168.60.15'
    iplist = ['192.168.60.125','192.168.60.12','192.168.60.10']
    # iplist = ['192.168.60.125']
    t1 = time.time()
    status = ping_status(ip1,iplist)
    t2 = time.time() - t1
    print t2

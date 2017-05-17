# coding=utf-8
__author__ = 'xuxin'

def test():
    #学：3 习：i，练 j  学习:3*10+i  练习:j*10+i  习习习：i*100+i*10+i
    for i in xrange(0,10):
        for j in xrange(0,10):
            # if (3*10+i)*(j*10+i) == i*100+i*10+i:
            for k in xrange(0,10):
                if (3*10+i)*(j*1+k*10) == i*100+i*10+i:
                    print i,j,k

def test2():
    #满足式子7*abcd = 4*dabc的最小值
    for i in xrange(0,10):
        for j in xrange(0,10):
            for k in xrange(0,10):
                for m in xrange(0,10):
                    a = 7*(i*1000+j*100+k*10+m)
                    b = 4*(m*1000+i*100+j*10+k)
                    if a == b:
                        print i,j,k,m

list = [{"process_name": "smss.exe", "pid": "316", "process_memory": "1196KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "csrss.exe", "pid": "520", "process_memory": "5464KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "wininit.exe", "pid": "580", "process_memory": "5304KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "csrss.exe", "pid": "600", "process_memory": "18916KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "winlogon.exe", "pid": "644", "process_memory": "8340KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "services.exe", "pid": "688", "process_memory": "9016KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "lsass.exe", "pid": "704", "process_memory": "12416KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "lsm.exe", "pid": "712", "process_memory": "6192KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "svchost.exe", "pid": "812", "process_memory": "9780KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "nvvsvc.exe", "pid": "932", "process_memory": "7456KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "QQPCRTP.exe", "pid": "996", "process_memory": "18144KB", "process_cpu": "0%", "process_cmd": "\"C:\\Program Files (x86)\\Tencent\\QQPCMgr\\10.2.15408.216\\QQPCRtp.exe\" -r"},
        {"process_name": "svchost.exe", "pid": "260", "process_memory": "8964KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "svchost.exe", "pid": "780", "process_memory": "20880KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "svchost.exe", "pid": "1012", "process_memory": "191472KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "svchost.exe", "pid": "1052", "process_memory": "34280KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "svchost.exe", "pid": "1192", "process_memory": "14716KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "svchost.exe", "pid": "1268", "process_memory": "17940KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "spoolsv.exe", "pid": "1492", "process_memory": "11772KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "svchost.exe", "pid": "1524", "process_memory": "8384KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "armsvc.exe", "pid": "1576", "process_memory": "4020KB", "process_cpu": "0%", "process_cmd": "\"C:\\Program Files (x86)\\Common Files\\Adobe\\ARM\\1.0\\armsvc.exe\""},
        {"process_name": "svchost.exe", "pid": "1596", "process_memory": "9716KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "aspnet_state.exe", "pid": "1616", "process_memory": "6428KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "FileZilla Server.exe", "pid": "1680", "process_memory": "4896KB", "process_cpu": "0%", "process_cmd": "\"D:\\Program Files (x86)\\FileZilla Server\\FileZilla Server.exe\""},
        {"process_name": "svchost.exe", "pid": "1744", "process_memory": "9900KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "inetinfo.exe", "pid": "1776", "process_memory": "15776KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "HeciServer.exe", "pid": "1820", "process_memory": "5816KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "MsDtsSrvr.exe", "pid": "1868", "process_memory": "25256KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "sqlservr.exe", "pid": "2012", "process_memory": "82552KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "sqlservr.exe", "pid": "2036", "process_memory": "43348KB", "process_cpu": "0%", "process_cmd": "\"D:\\Program Files (x86)\\Microsoft SQL Server\\MSSQL.1\\MSSQL\\Binn\\sqlservr.exe\" -sMSSQLSERVER"},
        {"process_name": "nvxdsync.exe", "pid": "1692", "process_memory": "18888KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "nvvsvc.exe", "pid": "1924", "process_memory": "13036KB", "process_cpu": "0%", "process_cmd": ""},
        {"process_name": "msmdsrv.exe", "pid": "2456", "process_memory": "41224KB", "process_cpu": "0%", "process_cmd": ""}]

if __name__ == '__main__':
    # test()
    test2()

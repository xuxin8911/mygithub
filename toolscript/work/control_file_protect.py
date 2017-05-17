#coding=utf-8
__author__ = 'xuxin'
import Globals
from ZenPacks.Aether.SSOC.tcpclient import TCPClient
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
import time,uuid,sys

#控制文件保护的运行或停止
class ActionCmd(ZenScriptBase):
    def control_file_protect(self,enabled,dest_ip):
        self.connect()
        dbpool = self.dmd._getOb('ZenSSOCDBSpool')
        conn = dbpool.connect()
        curs = conn.cursor()
        sql1 = "select virsh_id from cloud_virsh where virsh_ip = '%s'"%(dest_ip)
        curs.execute(sql1)
        result = curs.fetchall()
        if not result:
            return {'result':'false','desc':'device is not exist!'}
        dev_id = result[0][0]
        tcpclient = TCPClient('127.0.0.1',port=8899)
        # tcpclient = TCPClient('192.168.1.155',port=8899)
        tcpclient.connect()
        end = time.time() + 2
        while not tcpclient.connected:
            if time.time() > end:
                return {'result':'false','data':'agentforwardsvr not open!'}
            time.sleep(1)
        else:
            data = {}
            tcpclient.cliSock.setblocking(1) # 设置阻塞
            tcpclient.cliSock.settimeout(5)  #设置超时时间
            agent = uuid.uuid1() #通用唯一识别码
            ts = time.time()
            sendData = '''connect id="0" agent="%s" ts="%s"\r\n'''%(agent,ts)
            tcpclient.cliSock.send(sendData)
            ret_data = tcpclient.cliSock.recv(10240)
            errstring = ret_data.split(' ')[1]
            if errstring == 'errno="0"': #连接成功
                cmd = '''enable_auto_restore enabled="%s" target="%s" agent="%s"\r\n'''%(enabled,dev_id,agent)
                tcpclient.cliSock.send(cmd)
                End = '\r\n'
                total_data = []
                data = ''
                while True:
                    try:
                        data = tcpclient.cliSock.recv(10240)
                    except:
                        return {'result':'false','data':'linux_agent not open!'}
                    if End in data:
                        total_data.append(data[:data.find(End)])
                        break
                    total_data.append(data)
                    if len(total_data) < 1:
                        #check if end_of_data was split
                        last_pair = total_data[-2]+total_data[-1]
                        if End in last_pair:
                            total_data[-2] = last_pair[:last_pair.find(End)]
                            total_data.pop()
                            break
                ret_data = ''.join(total_data)
                if ret_data.startswith("auto_restore_res"):
                    return {'result':'success','data':'operate success!'}
                else:
                    return {'result':'false','data':ret_data}
if __name__ == "__main__":
    #eg: su - zenoss -c "python /usr/local/zenoss/zenoss/libexec/control_file_protect.py 1 '4ef54aa4-9a3b-411a-8155-cc667e8b4962'"
    enabled = sys.argv[1]
    dest_ip = sys.argv[2]
    a = ActionCmd()
    ret = a.control_file_protect(enabled,dest_ip)
    print ret


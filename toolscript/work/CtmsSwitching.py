#!/usr/local/zenoss/zenoss/bin/python
#coding:utf-8
#1.启动备
#	1。判断是否是物理机（虚拟机忽略）
#   2。是否已经启动备机（已经启动备机，则忽略）
#   3。获取同个域的虚拟机IP
#   3。循环检测是否是出于CTMS服务器分类下，如果已处于该分类，则换个虚拟机再试
#   4。将改变虚拟机的分类到CTMS服务器分类下
#   5。执行启动CTMS的命令
#   6。登记主备关系
#   7。重启zencommand
#2。停止备
#   1。 判断是否是物理机（虚拟机忽略）
#   2。 获取备机的ID
#   3。 删除主备关系
#   4.  停止CTMS
#   3。 移动到虚拟Linux服务器类下
#   4.  重启zencommand
__author__ = 'tangj'
from HttpHandler import HttpHandler
import logging
import time,os
import getopt
import subprocess
logging.basicConfig(filename="/usr/local/zenoss/zenoss/log/ctmsswitch.log",level=logging.DEBUG)
logger =logging.getLogger('ctmsswitch')

def help():
    print """
    ./CtmsSwitching.py -H device_ip -A action[stop or start]
    """
APP_CLASS = "CTMS"
class SwitchCTMS:
    def __init__(self,dev_ip):
        self.conn = None
        self.dev_ip = dev_ip
        self.rpc_handle = HttpHandler()
        self.rpc_handle.login()
        self.getDabaseConnect()

    def complieText(self,dev_ip,text):
        return self.rpc_handle.getResponseData("device_router","DeviceRouter","compile_text",[{"dev_ip":dev_ip,"text":text}])

    def getDeviceInfo(self,devclass = "/zport/dmd/Devices/",devIp=None):
        param = [{"start":0,
        	"limit":50,
            "dir":"ASC",
            "sort":"name",
            "params":"{\"productionState\":[\"1000\"]",
            "uid":devclass}]
        if devIp:
            param[0]["params"]= param[0]["params"] + ',"ipAddress":"'+devIp+'"}'
        else:
            param[0]["params"]= param[0]["params"]+"}"
        return self.rpc_handle.getResponseData("device_router","DeviceRouter","getDevices",param)

    def getDabaseConnect(self):
        text = '${device/db_ip} ${device/db_port} ${device/db_user} ${device/db_passwd}'
        result = self.complieText(self.dev_ip,text)
        if result:
            dbcfg = result.split()
            conn = None
            import MySQLdb
            try:
                self.conn = MySQLdb.connect(host=dbcfg[0], user=dbcfg[2],port=int(dbcfg[1]), passwd=dbcfg[3],db="ssoc",reconnect=1,init_command="SET NAMES utf8")
                self.conn.autocommit(1)
            except:
                logger.warning("连接数据库失败")
        else:
            logger.warning("获取数据库连接参数失败！%s可能不存在"%self.dev_ip)

    def DelBackDeviceInfo(self):
        logger.debug("being DelBackDeviceInfo")
        sql = 'select back_ip,back_id from cloud_master_back_info where master_ip = "%s"'%self.dev_ip
        self.conn.query(sql)
        result = self.conn.use_result()
        rows =  result.fetch_row(0,1)
        sql = 'delete from cloud_master_back_info where master_ip = "%s"'%self.dev_ip
        curs = self.conn.cursor()
        curs.execute(sql)
        logger.debug("end DelBackDeviceInfo")
        return rows

    def StopService(self,dev_ip):
        param = "${device/zCommandPassword} ${device/zCommandPort} ${device/zCommandUsername} ${device/zSybaseModelerOSUser}"
        param = self.complieText(dev_ip,param)
        if param:
            params_list = param.split()
            cmd = 'sudo sshpass -p %s ssh -p %s %s@%s su - %s -c "echo null_acb |stopctms;killall -9 ctms;echo ok"""'%(params_list[0],params_list[1],params_list[2],dev_ip,params_list[3])
            logger.info("exec command :%s"%cmd)
            cmd = "ls"
            p = subprocess.Popen(cmd,bufsize=1,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            logger.info("---StopCTMSService result----\n%s"%p.stdout.read())
        else:
            logger.warning("停止CTMS服务失败，编译停止命令出错")

    def StartService(self,dev_ip):
        param = "${device/zCommandPassword} ${device/zCommandPort} ${device/zCommandUsername} ${device/zSybaseModelerOSUser}"
        param = self.complieText(dev_ip,param)
        if param:
            params_list = param.split()
            cmd = 'sudo sshpass -p %s ssh -p %s %s@%s su - %s -c "echo null_acb |stopctms;killall -9 ctms;startctms;echo ok"""'%(params_list[0],params_list[1],params_list[2],dev_ip,params_list[3])
            logger.info("exec command :%s"%cmd)
            cmd = "pwd"
            p = subprocess.Popen(cmd,bufsize=1,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            logger.info("---StartService result----\n%s"%p.stdout.read())
        else:
            logger.warning("启动CTMS服务失败，编译停止命令出错")

    def ChangeDeviceClass(self,devid,newClass):
        #param = [{"uids":["/zport/dmd/Devices/Server/Webserver/Apache/devices/192.168.1.166"],"target":"/zport/dmd/Devices/Client"}]
        param = [{"uids":[devid],"target":newClass}]
        logger.info("修改设备%s的类型%s"%(devid,newClass))
        result = self.rpc_handle.getResponseData("acg_router","ACGRouter","changeDevCls",param)
        logger.info("修改设备%s的类型%s:返回%s"%(devid,newClass,result))


    def DoStartBack(self):
        #   2。是否已经启动备机（已经启动备机，则忽略）
        sql = 'select back_ip,back_id from cloud_master_back_info where master_ip = "%s"'%self.dev_ip
        self.conn.query(sql)
        result = self.conn.use_result()
        rows =  result.fetch_row(0,1)
        if len(rows) > 0:
            logger.warning("设备[%s]的备机已经启动，忽略启动备机操作"%self.dev_ip)
        else:
            #查询可用的备机
            sql = """select  virsh_id,virsh_ip from cloud_virsh a,
            (select domain_id from cloud_virsh where virsh_ip = "%s")c
            where a.domain_id = c.domain_id
            and a.device_type = 0
            and a.virsh_id not in(select back_id from cloud_master_back_info)"""%self.dev_ip
            self.conn.query(sql)
            result = self.conn.use_result()
            rows =  result.fetch_row(0,1)
            if len(rows)<= 0:
                logger.warning("设备[%s]的备机启动失败，没有空闲的备机"%self.dev_ip)
            else:
                result =self.getDeviceInfo(devIp=rows[0]["virsh_ip"])
                if result["totalCount"]>0:
                    logger.info("设备[%s]的备机[%s]开始启动"%(self.dev_ip,rows[0]["virsh_ip"]))
                    #启动CTMS
                    self.StartService(rows[0]["virsh_ip"])
                    #修改设备分类
                    back_devid = result["devices"][0]["uid"]
                    paths = back_devid.split("/")[0:-2]
                    paths.append(APP_CLASS)
                    newClass = "/".join(paths)
                    self.ChangeDeviceClass(back_devid,newClass)
                    #登记主备
                    curs = self.conn.cursor()
                    sql = "insert into cloud_master_back_info(back_id,back_ip,master_ip) values('%s','%s','%s')"%(back_devid,rows[0]["virsh_ip"],self.dev_ip)
                    curs.execute(sql)
                    #重启zendmd
                    os.system("zencommand restart")
                    logger.warning("设备[%s]的切换备机完成"%self.dev_ip)
                else:
                    logger.warning("设备[%s]的备机不存在"%self.dev_ip)


    def DoStopBack(self):
        import pydevd
        pydevd.settrace('127.0.0.1', port=7777, stdoutToServer=True, stderrToServer=True)
        backlist =self.DelBackDeviceInfo()
        if len(backlist) ==0:
            logger.warning("设备%s没有找到备机"%self.dev_ip)
        else:
            for back in backlist:
                #获取备份机的设备信息
                result = self.getDeviceInfo(devIp=back["back_ip"])
                #如果备机还存在
                if result["totalCount"]>0:
                    #移动到上一级设备类
                    paths= result["devices"][0]["uid"].split("/")
                    if paths[-3] == APP_CLASS:
                        paths = paths[0:-3]
                        self.ChangeDeviceClass(result["devices"][0]["uid"],"/".join(paths))
                    self.StopService(back["back_ip"])
                    os.system("zencommand restart")
                    logger.warning("设备[%s]的停止备机完成"%self.dev_ip)
                else:
                    logger.warning("设备[%s]的备机[%s]已不存在"%(self.dev_ip,back["back_ip"]))


if __name__=="__main__":
    hostip = ""
    action = ""
    opts, args = getopt.getopt(os.sys.argv[1:], "H:A:h", ["help"])
    for opt in opts:
        if opt[0] == "-h":
            help()
        elif opt[0] == "-H":
            hostip = opt[1]
        elif opt[0] == "-A":
            action = opt[1]
    s = SwitchCTMS(hostip)
    if action =="start":
        s.DoStartBack()
    elif action == "stop":
        s.DoStopBack()

#coding=utf-8
__author__ = 'xuxin'
'''
负载均衡
'''
import struct,socket,os,json,sys,traceback
import getopt
from HttpHandler import HttpHandler
import logging
import time
logging.basicConfig(filename="/usr/local/zenoss/zenoss/log/rest_ip.log",level=logging.DEBUG)
logger =logging.getLogger('rest_ip')
def set_member(ip,port,state,control_host,control_port):
    try:
        http = "http://%s:%s/quantum/v1.0/members/"%(control_host,control_port)
        get_cmd = 'curl %s'%http
        logger.info(get_cmd)
        try:
            str1 = os.popen(get_cmd).read().strip()
            member_list = json.loads(str1)
        except:
            logger.error('负载均衡配置有误，请检查!')
            return
        member_dict = {}
        #'{"id":"4","address":"10.0.0.4","port":"'$PORT'","pool_id":"2","admin_state":"0"}'
        #{'address': '-1062711085', 'vipId': '2', 'adminState': 0, 'poolId': '2', 'id': '3', 'port': '80'}
        for member in member_list:
            address = socket.inet_ntoa(struct.pack('!I',int(member['address'])))
            if address == ip and member['port'] == port:
                member_dict['id'] = member['id']
                member_dict['address'] = ip
                member_dict['port'] = member['port']
                member_dict['pool_id'] = member['poolId']
                if state == member['adminState']:
                    logger.warning('%s设备%s端口已经是%s状态！'%(ip,member['port'],state))
                    return 0
                else:
                    logger.warning('%s设备%s端口调整为%s状态！'%(ip,member['port'],state))
                member_dict['admin_state'] = state
        if not member_dict:
            logger.error('未发现指定负载均衡成员')
            return 0
        member_dict = json.dumps(member_dict)
        # requrl = "http://192.168.80.251:8080/quantum/v1.0/members/"
        cmd ="curl -X POST -d '%s' %s"%(member_dict,http)
        a = os.popen(cmd).read()   #python调用shell脚本，并返回结果
        b = a.rstrip()
        logger.info('%s'%b)
    except:
        logger.error(traceback.format_exc())

def get_sql_msg(src_ip,state):
    text = '${device/db_ip} ${device/db_port} ${device/db_user} ${device/db_passwd}'
    rpc_handle = HttpHandler()
    rpc_handle.login()
    result = rpc_handle.getResponseData("device_router","DeviceRouter","compile_text",[{"dev_ip":src_ip,"text":text}])
    if result:
        dbcfg = result.split()
        conn = None
        import MySQLdb
        try:
            conn = MySQLdb.connect(host=dbcfg[0], user=dbcfg[2],port=int(dbcfg[1]), passwd=dbcfg[3],db="ssoc",init_command="SET NAMES utf8")
            conn.autocommit(1)
            curs = conn.cursor()
            sql1 = "select b.mem_address,b.mem_port,a.control_address,a.control_port from cloud_virtual_server a " \
                   "LEFT JOIN cloud_virtual_member b on a.v_id = b.pool_id where b.mem_address='%s'"%src_ip
            curs.execute(sql1)
            conn.commit()
            result = curs.fetchall()
            #修改每个主机对应的端口状态
            for i in result:
                mem_address,mem_port,control_host,control_port = i
                set_member(mem_address,mem_port,str(state),control_host,control_port)
        except:
            logger.warning("连接数据库失败")
    else:
        logger.warning("获取数据库连接参数失败！%s可能不存在"%src_ip)

if __name__ == '__main__':
    #python /usr/local/zenoss/zenoss/libexec/rest_ip.py '10.0.0.4' '80' '0'
    src_ip = sys.argv[1]
    state = str(sys.argv[2])
    get_sql_msg(src_ip,state)
    now = time.localtime(time.time())
    now_time = time.strftime("%Y-%m-%d %H:%M:%S %Z", now)
    logger.info('%s\n\n'%now_time)

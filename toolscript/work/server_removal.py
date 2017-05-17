#coding=utf-8
__author__ = 'xuxin'

import MySQLdb
import ConfigParser
import logging

host = '127.0.0.1'
user = 'root'
passwd = 'ydsoc_*^#!(%)%'


logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='/home/xx/myapp.log',
                filemode='a+')
def update_record():
    cf = ConfigParser.ConfigParser()
    cf.read('/home/xx/server_removal.conf')
    zone = cf.get('config','availability_zone')
    intance_id = cf.get('config','instance_id')
    port_id = cf.get('config','net_port')
    ip_addr = cf.get('config','ip_addr')

    str1 = '要迁移虚拟机ip:{0}'.format(ip_addr)
    str2 = '要迁移到计算域:{0}'.format(zone)
    str3 = '云主机uuid:{0}'.format(intance_id)
    str4 = '网络端口id:{0}'.format(port_id)
    print '%s\n%s\n%s\n%s'%(str1,str2,str3,str4)
    enter = raw_input('请确认计算域和计算节点是否正确，Y or N:')
    if enter.upper() != 'Y':
        print '程序退出,请重新配置配置文件!'
        return
    logging.info(str1)
    logging.info(str2)
    logging.info(str3)
    logging.info(str4)
    conn1 = MySQLdb.connect(host=host,user=user,passwd=passwd,db='nova')
    cursor1 = conn1.cursor()
    sql1 = "update instances set host='{0}',availability_zone='{0}',launched_on='{0}',node='{0}' " \
           "where uuid = '{1}' ".format(zone,intance_id)
    print sql1
    cursor1.execute(sql1)
    conn1.commit()
    conn1.close()

    conn2 = MySQLdb.connect(host=host,user=user,passwd=passwd,db='neutron')
    cursor2 = conn2.cursor()
    sql2 = "update portbindingports set host='{0}' where port_id='{1}'".format(zone,port_id)
    cursor2.execute(sql2)
    conn2.commit()
    conn2.close()
    print sql2
    logging.info(sql1)
    logging.info('%s\n'%sql2)
    print '修改数据库成功,请按文档进行下一步操作!'

if __name__ == '__main__':
    update_record()



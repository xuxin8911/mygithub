#coding=utf-8
__author__ = 'xuxin'

import MySQLdb
import ConfigParser
import logging
import sys
snapshot_id = ''
snapshot_name = ''
host = '127.0.0.1'
user = 'root'
passwd = 'ydsoc_*^#!(%)%'
import re

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='/home/xx/snapshot.log',
                filemode='a+')

def add_snapshot(snapshot_id,snapshot_name):
    try:
        conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db='ssoc')
        cursor = conn.cursor()
        public = 1
        virsh_id = '9609878b-7f68-4b30-9e84-e72cf35c4350'
        domain_id = 'c383a80151614193a03ce02c6c14a83a'
        snapshot_time = 'now()'
        sql = "insert into cloud_snapshot(snapshot_id,snapshot_name,public,virsh_id,domain_id,snapshot_time) " \
               "values('{0}','{1}','{2}','{3}','{4}',{5})".format(snapshot_id,snapshot_name,public,virsh_id,domain_id,snapshot_time)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        logging.info(sql)
    except Exception,e:
        print e

if __name__ == '__main__':
    print '''
    此脚本仅适用没有种子机，直接建业务机，这时候没有快照的情况\n
    从openstack界面里面找到要用到的镜像的镜像ID和名称\n
    '''
    snapshot_id = raw_input('请输入镜像ID：')
    com = re.search('[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}', snapshot_id)
    if not com:
        print '镜像ID不对，请重新输入！'
    else:
        snapshot_name = raw_input('请输入镜像名称:')
        add_snapshot(snapshot_id,snapshot_name)
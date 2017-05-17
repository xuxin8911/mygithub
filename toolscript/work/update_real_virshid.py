#coding=utf-8
__author__ = 'xuxin'

import MySQLdb
import ConfigParser
import logging
import sys
snapshot_id = ''
snapshot_name = ''
host = '192.168.2.12'
user = 'root'
passwd = 'ydsoc_*^#!(%)%'
import re

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='/home/xx/update_real_virshid.log',
                filemode='a+')

def update_real_virshid(new_seed_id,old_seed_id):
    try:
        conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db='ssoc')
        cursor = conn.cursor()      
        sql1 = "update cloud_business_dir set business_virsh = '{0}' where business_virsh = '{1}'".format(new_seed_id,old_seed_id)
        sql2 = "update cloud_snapshot set virsh_id = '{0}' where virsh_id = '{1}'".format(new_seed_id,
                                                                                                      old_seed_id)
        sql3 = "update cloud_svn_dir set virsh_id = '{0}' where virsh_id = '{1}'".format(new_seed_id,
                                                                                                      old_seed_id)
        sql4 = "update cloud_seed_dir set seed_virsh = '{0}' where seed_virsh = '{1}'".format(new_seed_id,
                                                                                                      old_seed_id)
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        cursor.execute(sql4)
        conn.commit()
        conn.close()
        logging.info(sql1)
        logging.info(sql2)
        logging.info(sql3)
        logging.info(sql4)
        logging.info('\n')
    except Exception,e:
        print e

if __name__ == '__main__':
    print '''
    此脚本仅适种子机重建，修改种子机原来的快照，黑名单，白名单，以及同步目录virsh_id\n
       '''
    new_seed_id = raw_input('请输入新的种子机ID: ')
    com = re.search('[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}', new_seed_id)
    if not com:
        print '新的种子机id不对，请重新输入！'
    else:
        old_seed_id = raw_input('请输入原来种子机ID: ')
        com = re.search('[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}', old_seed_id)
        if not com:
            print '原来的种子机id不对，请重新输入！'
        update_real_virshid(new_seed_id,old_seed_id)
		
		
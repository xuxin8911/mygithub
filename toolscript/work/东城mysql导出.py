#coding=utf-8
__author__ = 'xuxin'
import time
import os
host = '127.0.0.1'
base_dir = '/home/dbbackup'
dir_name = time.strftime("%Y-%m-%d", time.localtime())
db_list = ['events','glance','jasperserver','keystone','neutron','nova','ssoc']

def export_db(username,passwd):
    path = '/home/dbbackup/{0}'.format(dir_name)
    if not os.path.exists(path):
        os.mkdir(path)
    for db_name in db_list:
        print '备份数据库到{0}...'.format(path)
        print '开始导出数据库{0}...'.format(db_name)
        cmd = "mysqldump -h{0} -u'{1}' -p'{2}' --opt -R {3} |gzip -9> {4}/{3}.sql.gz".format(host,username,passwd,db_name,path)
        p = os.popen(cmd)
        ret = p.read()
        if ret.strip():
            print ret
            break

if __name__ == '__main__':
    # host = raw_input('请输入服务器IP(127.0.0.1):')
    username = raw_input('请输入mysql账号:')
    passwd = raw_input('请输入mysql密码:')
    export_db(username,passwd)




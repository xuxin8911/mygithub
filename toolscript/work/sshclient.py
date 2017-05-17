#coding=utf-8
__author__ = 'xuxin'

import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cmd = '''su - oracle -c "sh /usr/local/bin/oracle_status.sh '/as sysdba'  /home/oracle/oinstall/product/11.2.0/dbhome_1 dcqxtbg"'''
client.connect('172.25.65.170', 22, username='root', password='Dcqxtbg2014*', timeout=4)
stdin, stdout, stderr = client.exec_command(cmd)
for std in stdout.readlines():
    print std
client.close()

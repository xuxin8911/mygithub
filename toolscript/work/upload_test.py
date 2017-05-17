#coding=utf-8
__author__ = 'xuxin'
# import Globals
# from Products.ZenUtils.ZenScriptBase import ZenScriptBase
import sys,time,urllib,urllib2,MySQLdb,httplib
from httplib2 import Http
from urllib import urlencode
import os,sys,time
import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase

class ActionCmd(ZenScriptBase):
    def upload_test(self,file,file_name,dest_ip,file_path):
        self.connect()
        test_data = {"file":file,'file_name':file_name,'dest_ip':dest_ip,'file_path':file_path}
        test_data_urlencode = urllib.urlencode(test_data)
        requrl = "http://192.168.1.166:8080/zport/dmd/JasperServerManager/upload_test_file"
        h = Http()
        content = h.request(requrl,"POST",test_data_urlencode)
        role_str = content[1]
        print role_str

    if __name__ == '__main__':
        # user_passwd = sys.argv[2]
        file = open('/home/xuxin/get_ip.py','rb')    #文件流
        dest_ip = '192.168.80.52'  #目标机器IP
        file_name = 'get_ip.py'    #文件名称
        file_path = '/home/xuxin'  #目标机器的路径
        print upload_test(file,file_name,dest_ip,file_path)

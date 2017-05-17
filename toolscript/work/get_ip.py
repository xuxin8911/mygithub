#!/usr/bin/python -E
#coding=utf-8
__author__ = 'xuxin'
# import Globals
# from Products.ZenUtils.ZenScriptBase import ZenScriptBase
import sys,time,urllib,urllib2,MySQLdb,httplib
from httplib2 import Http
from urllib import urlencode
class UMRouter():
    def get_user_ip(self,user_name):
        # print 'line 9',time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        # self.connect()
        # resultUserLst = []
        # userLst = self.dmd.zport.acl_users.searchUsers(cn='')
        # print 'line 13',time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        # user_dn = ''
        # for user in userLst:
        #     cn = user.get('cn','')
        #     if str(cn) == user_name:
        #         user_dn = user.get('dn','')
        # role_list = self.dmd.zport.acl_users.getGroups(dn=user_dn)  #获取角色列表
        # print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        # role_str = ''
        # for role in role_list:
        #     if role_str:
        #         role_str = ','.join((role_str,"'%s'"))%role[1]
        #     else:
        #         role_str = "'%s'"%role[1]
        # print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        # requrl = "http://192.168.1.166:8080/zport/dmd/cloud_router"
        # headerdata = {"Host":'192.168.1.166'}
        # conn = httplib.HTTPConnection('192.168.1.66')
        # conn.request(method="POST",url=requrl,body=test_data_urlencode,headerdata)
        # response = conn.getresponse()
        # res = response.read()
        # print res
        test_data = {"user_name":user_name}
        test_data_urlencode = urllib.urlencode(test_data)
        requrl = "http://127.0.0.1:8080/zport/acl_users/get_user_role"
        h = Http()
        content = h.request(requrl,"POST",test_data_urlencode)
        # print content

        role_str = content[1]
        conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='6d600acc6a2e4484',db='ssoc',port=3306)
        cur=conn.cursor()
        curs = conn.cursor()
        sql = "select a.virsh_ip from cloud_virsh a LEFT JOIN cloud_domain_role b on a.domain_id = b.domain_id " \
              "where b.role_id in (%s)"%role_str
        curs.execute(sql)
        result = curs.fetchall()
        try:
            ip = result[0][0]
            return ip
        except:
            return '没有对应ip'

if __name__ == '__main__':
    user_name = sys.argv[1]
    # user_passwd = sys.argv[2]
    um = UMRouter()
    print um.get_user_ip(user_name)
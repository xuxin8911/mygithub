#coding=utf-8
__author__ = 'xuxin'
'''
负载均衡配置
'''
import struct,socket,os,json,sys,traceback
import subprocess
host = '192.168.77.169'
def add_server(v_id,v_address,v_port):
    '''
    添加虚服务和连接池
    '''
    # sql1 = "insert into cloud_virtual_server(v_address,v_port) values('%s','%s')"
    # sql2 = "select last_insert_id()"
    # result = [[104]]
    # v_id = result[0][0]
    try:
        v_name = ''.join(('vip',str(v_id)))
        pool_name = ''.join(('pool',str(v_id)))
        curl_add_server = '''curl -X POST -d '{"id":"%s","name":"%s","protocol":"tcp","address":"%s","port":"%s"}' \
        http://%s:8080/quantum/v1.0/vips/'''%(v_id,v_name,v_address,v_port,host)
        print curl_add_server
        p = subprocess.Popen(curl_add_server, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        ret1 =  p.stdout.readlines()
        ret_dict = json.loads(ret1[len(ret1)-1])
        print ret1
        if not isinstance(ret_dict,dict):
            print '添加虚服务错误'
        curl_add_pool = '''curl -X POST -d '{"id":"%s","name":"%s","protocol":"tcp","vip_id":"%s"}' \
        http://%s:8080/quantum/v1.0/pools/ '''%(v_id,pool_name,v_id,host)
        print curl_add_pool
        p = subprocess.Popen(curl_add_pool, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        ret2 =  p.stdout.readlines()
        ret_dict = json.loads(ret1[len(ret2)-1])
        print ret2
        if not isinstance(ret_dict,dict):
            print '添加地址池错误'
        print 'success...'
    except:
        print traceback.format_exc()

def add_member(p_id,member_id,member_address,member_port):
    '''
    添加成员
    '''
    try:
        curl_add_member = '''curl -X POST -d '{"id":"%s","address":"%s","port":"%s","pool_id":"%s"}' \
        http://%s:8080/quantum/v1.0/members/'''%(member_id,member_address,member_port,p_id,host)
        print curl_add_member
        p = subprocess.Popen(curl_add_member, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        ret1 =  p.stdout.readlines()
        ret_dict = json.loads(ret1[len(ret1)-1])
        print ret1
        if not isinstance(ret_dict,dict):
            print '添加成员失败'
    except:
        print traceback.format_exc()

def delete_server(v_id):
    '''
    删除虚服务
    '''
    try:
        #查找连接池包含的成员
        get_pool_member = '''curl http://%s:8080/quantum/v1.0/pools/%s/members'''%(host,v_id)
        p = subprocess.Popen(get_pool_member, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        ret3 =  p.stdout.readlines()
        ret_list = json.loads(ret3[len(ret3)-1])
        print ret_list
        #删除成员
        if len(ret_list) > 0:
            for i in ret_list:
                member_id = i['id']
                delete_member(member_id)
        #删除地址池
        curl_del_pool = '''curl -X DELETE http://%s:8080/quantum/v1.0/pools/%s '''%(host,v_id)
        print curl_del_pool
        p = subprocess.Popen(curl_del_pool, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        ret2 =  p.stdout.readlines()
        ret_flag = ret2[len(ret2)-1]
        print ret2
        if ret_flag != '0':  #ret1[1] = 0成功  = -1失败
            print '删除地址池失败'
            return
        #删除虚服务
        curl_del_server = '''curl -X DELETE http://%s:8080/quantum/v1.0/vips/%s'''%(host,v_id)
        print curl_del_server
        p = subprocess.Popen(curl_del_server, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        ret1 =  p.stdout.readlines()
        ret_flag = ret1[len(ret1)-1]
        print ret1
        if ret_flag != '0':  #ret1[1] = 0成功  = -1失败
            print '删除虚服务失败'
            return
        print 'success...'
    except:
        print traceback.format_exc()

def delete_member(member_id):
    '''
    删除成员
    '''
    try:
        curl_del_member = '''curl -X DELETE http://%s:8080/quantum/v1.0/members/%s'''%(host,member_id)
        print curl_del_member
        p = subprocess.Popen(curl_del_member, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        ret1 =  p.stdout.readlines()
        ret_flag = ret1[len(ret1)-1]
        print ret1
        if ret_flag != '0':  #ret1[1] = 0成功  = -1失败
            print '删除成员失败'
            return
    except:
        print traceback.format_exc()

if __name__ == '__main__':
    #添加虚服务，连接池
    #python rest_balance.py 1 109 192.168.1.169 3307
    method = sys.argv[1]
    if method == '1':
        v_id = sys.argv[2]
        v_address = sys.argv[3]
        v_port = sys.argv[4]
        add_server(v_id,v_address,v_port)
    elif method == '2':
        #添加成员
        #python rest_balance.py 2 109 12 192.168.1.169 3307
        p_id = sys.argv[2]
        member_id = sys.argv[3]
        member_address = sys.argv[4]
        member_port = sys.argv[5]
        add_member(p_id,member_id,member_address,member_port)
    elif method == '3':
        #删除虚服务
        #python rest_balance.py 3 109
        id = sys.argv[2]
        delete_server(id)
    elif method == '4':
        #删除成员
        #python rest_balance.py 4 9
        id = sys.argv[2]
        delete_member(id)
    else:
        print '输入参数有误！'


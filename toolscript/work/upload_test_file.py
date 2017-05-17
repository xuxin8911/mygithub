#coding=utf-8
__author__ = 'xuxin'
import os
import base64
import subprocess

#上传文件到目标机器
def upload_test_file(file,file_name,dest_ip,file_path):
    '''
    file:文件流base64编码
    file_name:文件名称
    dest_ip：目标机器IP
    file_path：要上传到的目标机器路径
    '''
    file_dir = '/home/zenoss/upload_test_file'
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    file_local = '/'.join((file_dir,file_name))
    with open(file_local, 'wb') as fp:
        fp.write(file.read())
    cmd = "scp -r %s %s:%s"%(file_local,dest_ip,file_path)
    print cmd
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        ret =  p.stdout.read()
        if ret.strip():
            flag = False
            error_info = ret
        else:
            flag = True
            error_info = '上传文件成功'
    except Exception,e:
          flag = True
          error_info = e
    finally:
         return {'result':flag,'error_info':error_info}

if __name__ == '__main__':
    file = open('/home/xuxin/get_ip.py','rb')    #文件流
    dest_ip = '192.168.80.52'  #目标机器IP
    file_name = 'get_ip.py'    #文件名称
    file_path = '/home/xuxin'  #目标机器的路径
    result = upload_test_file(file,file_name,dest_ip,file_path)
    file.close()
    print result
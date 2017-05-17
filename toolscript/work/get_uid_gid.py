__author__ = 'xuxin'
'''
获取Linux用户的用户名密码
'''
import os
def get_uid_gid():
    if not os.path.exists('/home/zenoss/script'):
        #默认创建的目录权限是777，所有用户能执行
        os.mkdir('/home/zenoss/script')
        #获取用户的uid，gid
        cmd1 = 'id -u zenoss'
        cmd2 = 'id -g zenoss'
        uid = int(os.popen(cmd1).read().rstrip())
        gid = int(os.popen(cmd2).read().rstrip())
        #修改/home/zenoss/script目录的用户用户组
        os.chown('/home/zenoss/script',uid,gid)
        return uid,gid

if __name__ == '__main__':
    get_uid_gid()

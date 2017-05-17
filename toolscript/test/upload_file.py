# coding=utf-8
__author__ = 'xuxin'
from super_test import public_func
from super_test import __private_fuc

def upload_file():
    file = open('e:\\a.txt','rb')
    print file

if __name__ == '__main__':
    upload_file()
    __private_fuc()
#coding=utf-8

import os
LOG_APP = 'E:\\vmware'
uuid = '5f143934-9088-4d38-b873-287e5726378d'


def app_check():
    inst_app_path = ''.join((LOG_APP,uuid))
    print
    for i in os.path.walk(inst_app_path):
        print i



if __name__ == '__main__':
    pass

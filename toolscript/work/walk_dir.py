#coding=utf-8
__author__ = 'xuxin'

import os
import time
rootdir = "F:\\testwalk"                                   # 指明被遍历的文件夹
log_name = 'filecount.txt'

def time_transform(path):
    timestamp = os.path.getmtime(path)
    time_array = time.localtime(timestamp)
    transform_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return transform_time

def num_trancesform(num):
    pass

def count_file(root_dir):
    total_size = 0
    total_file_num = 0
    f = open(log_name,'w')
    root_log =  '%s 目录下的文件:\n'%(rootdir)
    f.write(root_log)
    for parent,dirnames,filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        if parent == 'C:\\Python27':
            continue
        parent_size = 0
        file_num = 0
        # print parent + ' 的目录:'
        for dirname in  dirnames:                    #输出文件夹信息
            dir_path = os.path.join(parent,dirname)
            dir_time = time_transform(dir_path)
            # print  dir_time + '   <DIR>             ' + dir_path

        for filename in filenames:                        #输出文件信息
            file_path = os.path.join(parent,filename) #输出文件路径信息
            file_size = os.path.getsize(file_path)
            file_time = time_transform(file_path)
            file_log =  file_time + '              '+  '{:,}'.format(file_size).ljust(30) +file_path+'\n'
            f.write(file_log)
            total_size += file_size
            parent_size += file_size
            file_num += 1
            total_file_num += 1
        # print '                      %s 个文件          %s 字节'%(file_num,parent_size)

    count_log =  '所列文件总数:  %s 个文件   %s 个字节\n'%(total_file_num,'{:,}'.format(total_size))
    f.write(count_log)
    f.close()

if __name__ == '__main__':
    count_file(rootdir)

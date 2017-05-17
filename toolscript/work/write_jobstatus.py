#coding=utf-8
__author__ = 'xuxin'
import os

def write_job_status(jobid,value):
    if not os.path.exists('/tmp/jobstatus'):
        os.mkdir('/tmp/jobstatus')
    file_name =jobid
    dir_name = '/tmp/jobstatus'
    f = open(os.path.join(dir_name,file_name),'w+')
    filename = f.name
    f.write(value)
    f.close()

def delete_job_status(jobid):
    file_name =jobid
    dir_name = '/tmp/jobstatus'
    file = '/'.join((dir_name,file_name))
    os.remove(file)

def read_job_status(jobid):
    file_name =jobid
    dir_name = '/tmp/jobstatus'
    f = open(os.path.join(dir_name,file_name))
    file = f.readline()
    return file

if __name__ == '__main__':
    jobid = 'CloudJobStatus_a86c5773-46c6-4eb7-b8fb-d963b95d4f6f'
    job_dict = {'rate':'80%','desc':'创建与管理域的路由接口成功!'}
    write_job_status(jobid,str(job_dict))
    ret_file = read_job_status(jobid)
    print eval(ret_file)
    delete_job_status(jobid)

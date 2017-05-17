#coding=utf8
__author__ = 'xuxin'
import re
def get_cmd_result(result):
        list1 = result.split(',')
        ret_dict = {}
        try:
            for i in list1:
                ds = re.search("=",i).start()
                ret_dict[i[:ds]] = i[ds+1:]
        except:
            ret_dict = 'error'
        exec_result = ret_dict

a = 'id=b1549d75-ac2e-4e50-8263-6cf01a3281b9'
#get_cmd_result(a)
def get_string():
    str1 = '''id=0f8ee34e68b2451bbde6e8f877d7a3eb,user=testdomain7,passwd=NTgyNTk3MjM2ZGZmY2NkODc3YzY1Yjk4Cg==
<<<<<JOBMESSAGE>>>>> Job completed at 2014-02-21 14:10:28. Result: success.
<<<<<EOF>>>>><<<<<JOBMESSAGE>>>>> -------------创建安全域成功1！---------------------------创建安全域成功2！--------------
<<<<<EOF>>>>>'''
    list1 = str1.split('<<<<<JOBMESSAGE>>>>>')
    ret_list = []
    for i in list1:
        list2 = i.split('<<<<<EOF>>>>>')
        for j in list2:
            if j:
                ret_list.append(j)
    print ret_list
    logMsg = ''.join(ret_list)
    pass
if __name__ == '__main__':
    get_string()
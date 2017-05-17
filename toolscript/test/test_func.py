#coding=utf-8
__author__ = 'xuxin'

import sys
def test():
    return 'test'
def test2():
    return 1,2,3

def test3(a,b=True):
    print a,b

def test4(output):
    out_list = output.split('\r\n')
    path_list = []
    for i in out_list:
        for j in xrange(1,len(i)):
            if i[j] != ' ':
                path = ''.join(('"',i[j:],'"'))
                path_list.append(path)
                break
    path = ' '.join(path_list)
    return path

if __name__ == '__main__':
    output = '?   D:\\svn_test\campy01\r\n?      D:\\svn_test\sdsd 123\r\n'
    print test4(output)

    #
    # print sys.argv
    # try:
    #     if sys.argv[1] == '123':
    #         print test()
    # except:
    #     print 'unknow error'
    # a,b,c = test2()
    # import traceback
    # try:
    #     str1 = '1'
    #     i1 = 2
    #     str2 = str1+i1
    # except:
    #     print traceback.format_exc(0)
    #     print '---------------------------'
    #     print traceback.format_exc()


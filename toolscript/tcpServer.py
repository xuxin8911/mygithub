#coding=utf-8
__author__ = 'xuxin'
from socket import *
from time import ctime
import os
HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)
filepath = '/usr'
while True:
    # print 'waiting for connection...'
    print filepath
    tcpCliSock, addr = tcpSerSock.accept()
    # print '...connected from:', addr
    tcpCliSock.send(filepath)
    data = tcpCliSock.recv(BUFSIZ)
    print data
    # filepath = ' '
    tcpCliSock.close()
tcpSerSock.close()
        # try:
        #     filepath = data
        #     fileList = os.listdir(filepath)
        #     fileList2 = []  #绝对路径
        #     for i in fileList:
        #         print i
        #         print filepath
        #         path = ''.join([filepath,i])
        #         fileList2.append(path)
        #     # return fileList2
        #     tcpCliSock.send('[%s] %s' %(ctime(), fileList2))
        #     print 'success ------------------'
        # except:
        #     tcpCliSock.send('[%s] %s' %(ctime(), 'error'))
        #     print 'error--------------'

#coding=utf-8
__author__ = 'xuxin'
from socket import *
import os
# HOST = '192.168.5.217'
HOST = '192.168.1.153'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)


# while True:
# tcpCliSock = socket(AF_INET, SOCK_STREAM)
# tcpCliSock.connect(ADDR)
# print 'tc----------'
# data = 'send'
# if not data:
#     break
# tcpCliSock.send(data)
while True:
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    data1 = tcpCliSock.recv(BUFSIZ)
    print data1
    if not data1:
        tcpCliSock.send('')
    if data1 == ' ':
       tcpCliSock.send('')
    filepath = data1
    fileList = os.listdir(filepath)
    fileList2 = []  #绝对路径
    for i in fileList:
        # print i
        # print filepath
        path = ''.join([filepath,i])
        fileList2.append(path)
    tcpCliSock.send(str(fileList2))
    tcpCliSock.close()
tcpCliSock.close()

# coding=utf-8
__author__ = 'xuxin'

from socket import *
from time import ctime

HOST = ''
PORT = 8888
BUFSIZE = 1024
ADDR = (HOST,PORT)

tcpSerSock = socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    print 'waiting for connection...'
    tcpCliSock,addr = tcpSerSock.accept()
    print '...connected from :',addr
    while True:
        data = tcpCliSock.recv(BUFSIZE)
        if not data:
            break
        send_msg = '[%s] %s'%(ctime(),data)
        print send_msg
        tcpCliSock.send(send_msg)
tcpCliSock.close()
tcpSerSock.close()
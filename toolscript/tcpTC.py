#coding=utf-8
__author__ = 'xuxin'
from socket import *

host = '192.168.1.153'
port = 8888
bufsize = 1024

#开启套接字
tcpCliSock = socket(AF_INET, SOCK_STREAM)
#连接到服务器
tcpCliSock.connect((host, port))

data = 'send data'
tcpCliSock.send(data)
response = tcpCliSock.recv(bufsize)
print response
tcpCliSock.send('send data2')
tcpCliSock.close()
# while True:
#     #等待输入
#     data = raw_input('> ')
#     if not data:
#         break
#     #发送信息
#     tcpCliSock.send(data)
#     #接收返回信息
#     response = tcpCliSock.recv(bufsize)
#     if not response:
#         break
#     print response
# tcpCliSock.close()
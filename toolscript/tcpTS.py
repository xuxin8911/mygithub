#coding=utf-8
__author__ = 'xuxin'
'''
TCP服务端
'''
from socket import *   #引入socket的所有
from time import ctime   #时间戳函数，用于实现服务器的功能

HOST = '192.168.1.153' #主机地址
PORT = 8888         #端口号
BUFSIZE = 2048      #缓存区大小，单位是字节，这里设定2K
ADDR = (HOST,PORT)   #链接地址

tcpSerSock = socket(AF_INET,SOCK_STREAM)  #创建一个TCP套接字
tcpSerSock.bind(ADDR)   #绑定地址
tcpSerSock.listen(5)   #最大连接数为5

while True:  #无限循环
    print ('客户端连接。。。')   #显示文本信息
    tcpCliSock,addr=tcpSerSock.accept()
    print ('connect success:',addr)
    while True:
        data = tcpCliSock.recv(BUFSIZE)
        print '接收数据为:',data
        if not data:
            break
        tcpCliSock.send('[%s] %s'%(ctime(),data))

tcpCliSock.close()  #关闭连接
# tcpSerSock.close() #关闭服务器







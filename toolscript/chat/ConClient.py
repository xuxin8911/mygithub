#coding=utf-8
#简单tcp连接实例
__author__ = 'xuxin'
import socket
s = socket.socket()
s.connect(('192.168.1.153',7000))  #与服务器程序ip地址和端口号相同
s.send('hello is me')
data = s.recv(512)
s.send('hihi')
s.close()
print 'the data received is',data


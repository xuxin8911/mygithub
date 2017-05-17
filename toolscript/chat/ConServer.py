#coding=utf-8
__author__ = 'xuxin'
import socket
s = socket.socket()
s.bind(('192.168.1.153',7000))
s.listen(100)
print 'wait for connect...'
cs,address = s.accept()
print 'got connect from ',address
r1= cs.recv(512)
print r1
cs.send('byebye')
r2 = cs.recv(512)
print r2
cs.close()
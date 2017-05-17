#coding=utf-8
__author__ = 'xuxin'
'''
python与聊天程序，开两个线程，即是客户端，也是服务器
'''
import socket
import threading
import re

def service():
    s = socket.socket()
    s.bind(('192.168.1.153',7000))
    s.listen(5)
    conn,addr = s.accept()
    while True:
        print '[%s:%d] send a message to me: %s'%(addr[0],addr[1],conn.recv(1024))
    s.close()

def client():
    c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    c.connect(('192.168.1.153',7000))
    while True:
        sms = raw_input('Input the message you want to send:')
        c.sendall(sms)
    c.close()

if __name__ == '__main__':
    ser = threading.Thread(target = service)
    clt = threading.Thread(target = client)
    ser.start()
    clt.start()
    ser.join()
    clt.join()


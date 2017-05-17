__author__ = 'Administrator'
import struct,socket

def ipToInt(ip):
    return struct.unpack('!I',socket.inet_aton(ip))[0]

def intToIp(i):
    return socket.inet_ntoa(struct.pack('!I',i))

if __name__=='__main__':
    i = (2130706433,)
    i = i[0]
    print intToIp(i)
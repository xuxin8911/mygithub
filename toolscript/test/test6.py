#coding=utf-8
__author__ = 'xuxin'
import traceback
try:
    a = 1
    b = 0
    print a/b
    print 'line 7'
except:
    print 'line 9'
    print traceback.format_exc()

def get_local_ip(ifname = 'eth0'):
    import socket, fcntl, struct
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))
    ret = socket.inet_ntoa(inet[20:24])
    return ret

print get_local_ip()
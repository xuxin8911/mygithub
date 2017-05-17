__author__ = 'Administrator'

#!/usr/bin/python

"""
Phllip Calvin's python-traceroute.py, from http://gist.github.com/502451
based on Leonid Grinberg's traceroute, from
http://blog.ksplice.com/2010/07/learning-by-doing-writing-your-own-traceroute-in-8-easy-steps/
"""

import socket
import struct
import sys
import time
import subprocess
# import ip
import traceback

# We want unbuffered stdout so we can provide live feedback for
# each TTL. You could also use the "-u" flag to Python.
IPOPT_RR = 7
IPOPT_MINOFF = 4

class flushfile(file):
    def __init__(self, f):
        self.f = f
    def write(self, x):
        self.f.write(x)
        self.f.flush()

def traceroute(dest_name):
    dest_addr = socket.gethostbyname(dest_name)
    port = 33434
    max_hops = 30
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    while True:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        # send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        # send_socket.setsockopt(socket.IPPROTO_IP,socket.IP_OPTIONS,1024)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        #Build the GNU timeval struct (seconds, microseconds)
        timeout = struct.pack("ll", 5, 0)

        # Set the receive timeout so we behave more like regular traceroute
        recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)

        recv_socket.bind(("", port))
        # sys.stdout.write(" %d  " % ttl)
        send_socket.sendto("", (dest_name, port))
        curr_addr = None
        curr_name = None
        finished = False
        tries = 3

        while not finished and tries > 0:
            try:
                _, curr_addr = recv_socket.recvfrom(512)
                finished = True
                curr_addr = curr_addr[0]
                try:
                    curr_name = socket.gethostbyaddr(curr_addr)[0]
                except socket.error:
                    curr_name = curr_addr
            except socket.error as (errno, errmsg):

                tries = tries - 1
                # sys.stdout.write("* ")
                print ('%s *.'%ttl)

        send_socket.close()
        recv_socket.close()

        if not finished:
            pass

        if curr_addr is not None:
            curr_host = "%s (%s)" % (curr_name, curr_addr)
        else:
            curr_host = ""
        # sys.stdout.write("%s\n" % (curr_host))
        print "%s  %s\n" % (ttl,curr_host)

        ttl += 1
        if curr_addr == dest_addr or ttl > max_hops:
            break
        # break

def cmd(host):
    cmd = 'tracert %s'%ip
    p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    r1 =  p1.stdout.readlines()
    # sys.stdout.write('%s\n'%str(r1))
    print "%s\n" % (str(r1))

if __name__ == "__main__":
    # from pydev import pydevd
    # pydevd.settrace('192.168.1.153',port=7000,stdoutToServer=True,stderrToServer=True)
    host= '202.97.64.37'
    start_time = time.time()
    try:
        traceroute(host)
    except:
        print traceback.format_exc()
    end_time1 = time.time()
    # sys.stdout.write('%s\n'%(end_time1 - start_time))
    print end_time1 - start_time
    # cmd(ip)
    # end_time2 = time.time()
    # sys.stdout.write('%s\n'%(end_time2 - end_time1))


__author__ = 'Administrator'
import socket
import struct
IPOPT_OPTVAL = 0
IPOPT_OLEN = 1
IPOPT_OFFSET = 2
IPOPT_RR = 8
IPOPT_MINOFF = 4
NROUTES =  9

def checksum(source_string):
    sum = 0
    countTo = (len(source_string)/2)*2
    count = 0
    while count<countTo:
        thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
        sum = sum + thisVal
        sum = sum & 0xffffffff
        count = count + 2
    if countTo<len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff
    sum = (sum >> 16)  +  (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def get_head():
    packet = struct.pack("!BBHHH", 8, 0, 0, 0, 0)
    chksum=checksum(packet)
    packet = struct.pack("!BBHHH", 8, 0, chksum, 0, 0)

    head_len = 3 + 4*NROUTES + 1
    head = bytearray(head_len)
    head[0]=1
    head[1] = 7
    head[2]=39
    head[3]=8
    # head[4] = 192
    # head[5] = 168
    # head[6] = 1
    # head[7] = 153
    return packet,head

def print_buf_h(buf,dest_name):
    a = ""
    def list_to_ip(ip_int):
        ip =  '.'.join((str(int(ip_int[0],16)),str(int(ip_int[1],16)),str(int(ip_int[2],16)),str(int(ip_int[3],16))))
        return ip
    for b in bytearray(buf):
        a = a+ "%x "%b
    buf_list = a.split(' ')
    if buf_list[21] == '27':
        start = 27
    elif buf_list[22] == '27':
        start = 28
    print buf_list
    ip_list = []
    print a
    for n in xrange(0,8):
        ip_str = buf_list[start+n*4:start+(n+1)*4]
        ip =list_to_ip(ip_str)
        ip_list.append(ip)
        if ip == dest_name:
            break
    print ip_list



def main(dest_name):
    print 'dest_name = ',dest_name
    dest_addr = socket.gethostbyname(dest_name)
    port = 33434
    max_hops = 30
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    # send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, icmp)
    packet,head = get_head()
    send_socket.setsockopt(socket.IPPROTO_IP,socket.IP_OPTIONS,str(head))
    send_socket.setblocking(1)
    send_socket.settimeout(3)
    for i in xrange(0,10):
        send_socket.sendto(packet, (dest_name, 1))
    try:
        n = 0
        while True:
            print n
            n += 1
            buf,addr =  send_socket.recvfrom(2048)
            print buf,addr
            if addr[0] == dest_name:
                print_buf_h(buf,dest_name)
                break
            if n > 10:
                break
    except socket.error:
        pass
    finally:
        send_socket.close()

if __name__ == "__main__":
    import time
    start_time = time.time()
    # host = '198.6.8.10'
    host = '198.2.21.10'
    # host= '202.97.64.137'
    # host = '192.168.1.155'
    # host = '180.97.33.107'
    # host = '180.97.33.108'
    # host = '113.106.43.94'
    # host = '192.168.1.166'
    main(host)
    end_time = time.time()
    print end_time - start_time
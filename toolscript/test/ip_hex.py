__author__ = 'Administrator'

def ip_to_hex(ip):
    str_hex = ''
    for i in ip.split('.'):
        hex_i = hex(int(i))
        str_hex_i = str(hex_i)[2:]
        if len(str_hex_i) == 1:
            str_hex_i = ''.join(('0',str_hex_i))
        str_hex = ''.join((str_hex,str_hex_i))
    return ''.join(('0x',str_hex))



if __name__ == '__main__':
    ip = '172.168.44.1'
    print ip_to_hex(ip)
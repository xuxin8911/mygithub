#coding=utf-8
__author__ = 'xuxin'

import socket
import sys
import getopt

#公司测试
HOST = '192.168.66.178'
PORT = 9876
TIMEOUT = 30

#东城OA
HOST = '192.168.0.72'
PORT = 9876
TIMEOUT = 30

def usage():
    print 'send_message.py usage:'
    print '--manageIp: manageIp'
    print '--lastTime: lastTime'
    print '--eventClass: eventClass'
    print '--summary: summary'
    print '--phone: phone eg: 18811111111,18822222222'
    print '--test: test'

def send_message(note):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # msg = '13927495692:hello word!'
    address = (HOST,PORT)
    try:
        s.sendto(note.decode('utf-8').encode('gbk'),address)
        s.settimeout(TIMEOUT)
        print s.recv(1024)
    except Exception,e:
        print 'test'
        if e.errno == 10054:
            print '错误代码(%s):请检查服务器是否开启!'%e.errno
        else:
            print '错误代码(%s):%s'%(e.errno,e.message)
    finally:
        s.close()

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'h:', ['help=','manageIp=', 'lastTime=', 'eventClass=','summary=','phone=','test='])
        note = ''
        for o, a in opts:
            if o in ('-h', '--help'):
                usage()
                sys.exit(1)
            elif o in ('--manageIp',):
                manageIp = a
            elif o in ('--lastTime',):
                lastTime = a
            elif o in ('--eventClass',):
                eventClass = a
            elif o in ('--summary',):
                summary = a
            # elif o in ('--message',):
            #     message = a
            elif o in ('--phone',):
                phone = a
            elif o in ('--test',):
                note = '18664939321:192.168.1.166在2016051010:01错误,事件类型:/Status/Ping,摘要:测试是打发斯蒂芬阿斯蒂芬234234是打发地方地方啊撒地方撒地方2大声点发的发水电费撒大大发撒旦法是打发斯蒂芬按时地方4单方事故电饭锅'
        for p in phone.split(','):
            note = '{0}:设备{1}在{2}发生错误,事件类型:{3},摘要:{4}'.format(p,manageIp,lastTime,eventClass,summary)
            print note
            print len(note)
            send_message(note)
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)


if __name__ == '__main__':
    main(sys.argv)

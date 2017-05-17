# coding:utf-8
import urllib2
import urllib
import logging
import getopt
import sys
import threading
import time
import os

# phone='18801141438,18899778221,18514254886,18518153393,18510665393,13501378390,13661067804,13466589259,13641197648,18701689390,13260104045,13521119987,13521119987,18664939321'
phone = '18664939321,18664939321'

logging.basicConfig(filename="/usr/local/zenoss/zenoss/log/send_sms.log", filemode="a+",
                    format="%(asctime)s-%(name)s-%(levelname)s-%(message)s", level=logging.INFO);
log = logging.getLogger("sms")


def exec_send(data, txt, i):
    try:
        f = urllib2.urlopen(url='http://www.ztsms.cn:8800/sendSms.do', data=urllib.urlencode(data))
        log.info("send_sms:\n%s\nto %s return %s", txt, i, f.read())
        f.close()
        os.popen('wget http://127.0.0.1:8080')
    except Exception,e:
        print e


def send_sms(txt):
    threads = []
    for i in phone.split(','):
        data = {'username': 'tangj',
                'password': 'Aether_12345678',
                'content': txt,
                'mobile': i,
                'productid': '887362'}

        #        f = urllib2.urlopen(url='http://www.ztsms.cn:8800/sendSms.do',data=urllib.urlencode(data))
        # print data
        #        log.info("send_sms:\n%s\nto %s return %s",txt,i,f.read())
        #        print "send_sms:\n%s\nto %s return %s"%(txt,i,f.read())
        #        f.close()
        # log.info("send_sms:%s,to %s\n\n",txt,i)
        t = threading.Thread(target=exec_send, args=(data, txt, i))
        threads.append(t)
    for i in threads:
        i.setDaemon(i)
        i.start()
        time.sleep(0.5)


def main(argv):
    try:
        note = ''
        clearFirstTime = None
        opts, args = getopt.getopt(argv[1:], 'h:', ['help=', 'device=', 'component=', 'severityString=', 'firstTime=',
                                                    'clearFirstTime=', 'summary=', 'eventKey='])
        for o, a in opts:
            if o in ('-h', '--help'):
                sys.exit(1)
            elif o in ('--device',):
                device = a
            elif o in ('--component',):
                component = a
            elif o in ('--severityString',):
                severityString = a
            elif o in ('--firstTime',):
                firstTime = a
            elif o in ('--clearFirstTime',):
                clearFirstTime = a
            elif o in ('--summary',):
                summary = a
            elif o in ('--eventKey',):
                eventKey = a

        if not clearFirstTime is None:
            note = """故障恢复提醒：
设备：%s
级别：%s
事件关键字：%s
事件已修护：%s
修复时间：%s""" % (device, severityString, eventKey, summary, clearFirstTime)
        else:
            note = """故障报警：
设备：%s
级别：%s
事件关键字：%s
事件描述：%s
发生时间：%s""" % (device, severityString, eventKey, summary, firstTime)
        print note
        send_sms(note)
    except getopt.GetoptError, err:
        print str(err)
        log.error(str(err))
        sys.exit(2)


if __name__ == '__main__':
    main(sys.argv)

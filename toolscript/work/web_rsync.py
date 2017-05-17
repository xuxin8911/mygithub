#coding=utf-8
__author__ = 'xuxin'

import os
import logging
import time

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='web_sync.log',
                filemode='w+')

cmd = "rsync -arvz 192.168.2.63::linux_agent.024b290b26a4b98724fb638e8803a9fb/web31/subject/n1/n31 /usr/local/apache/htdocs/web31/subject/n1"
def run():
    t1 = time.time()
    ret = os.popen(cmd).read()
    t2 = time.time()
    logging.info( 'use time %s'%(t2-t1))

if __name__ == '__main__':
    logging.info( 'start run...')
    logging.info('exec %s'%cmd)
    while True:
        run()
        time.sleep(10)
    logging.info( 'end run...')

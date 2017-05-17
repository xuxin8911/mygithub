#coding=utf-8
__author__ = 'xuxin'

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import threading

def watch(flag):
    if flag == 1:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
    elif flag == 2:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S')
    # path = sys.argv[1] if len(sys.argv) > 1 else '.'
    # logging.basicConfig(level=logging.INFO,
    #                         format='%(asctime)s - %(message)s',
    #                         datefmt='%Y-%m-%d %H:%M:%S')
    print flag
    path = 'd:\\home'
    event_handler = LoggingEventHandler()
    print '24'
    observer = Observer()
    print '26'
    observer.schedule(event_handler, path, recursive=True)
    print '28'
    observer.start()
    print '30'
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print '36'
        observer.stop()
    observer.join()

if __name__ == "__main__":
    threads = []
    t1 = threading.Thread(target=watch,args = (1,))
    threads.append(t1)
    t2 = threading.Thread(target=watch,args=(2,))
    # threads.append(t2)
    for t in threads:
        t.setDaemon(True)
        t.start()
    print 'end...'
    while True:
        time.sleep(1)
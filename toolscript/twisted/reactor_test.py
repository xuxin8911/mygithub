# coding=utf-8
__author__ = 'xuxin'

import time
from twisted.internet import reactor

def processPage(page):
    for i in range(3):
        print 'i = ',i
    finnishProcessing()

def logError(error):
    print error
    finnishProcessing()

def finnishProcessing(value):
    print 'Shutting down...'
    reactor.stop()

url = 'http://google.com'
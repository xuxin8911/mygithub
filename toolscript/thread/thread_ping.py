#coding=utf-8
__author__ = 'xuxin'

from threading import Thread
import subprocess
from Queue import Queue

num_threads = 3
ips = ['192.168.1.155','192.168.1.166','192.168.1.164']


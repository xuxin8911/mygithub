# coding=utf-8
__author__ = 'xuxin'
'''
装饰符@示例
'''

def spamrun(fun):
    def sayspam(*args):
        fun(*args)
        print "spam,spam,spam"
    return sayspam

@spamrun
def useful(a,b):
    print a*2+b*2

# useful = spamrun(useful)
c
useful(3,4)



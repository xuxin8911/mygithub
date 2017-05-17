#coding=utf-8
__author__ = 'xuxin'

def de(f):
    print 'de'
    def __call__(t):
        print '--------'
        return f(t)
    return __call__

def func1(t):
    print 'func1'

@de
def func2(t):
    print 'func2'
    print t
    return '123'

@func1
def func3():
    print 'func3'

t = 'test'
print func2(t)
print func3
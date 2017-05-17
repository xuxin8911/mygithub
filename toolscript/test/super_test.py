# coding=utf-8
__author__ = 'xuxin'

class A(object):
    def __init__(self):
       print "enter A"
       print "leave A"

class B(object):
    def __init__(self):
       print "enter B"
       print "leave B"

class C(A):
    def __init__(self):
       print "enter C"
       super(C, self).__init__()
       print "leave C"

class D(A):
    def __init__(self):
       print "enter D"
       super(D, self).__init__()
       print "leave D"

class G(A):
    def __init__(self):
       print "enter G"
       super(G, self).__init__()
       print "leave G"


class E(B, C):
    def __init__(self):
       print "enter E"
       B.__init__(self)
       C.__init__(self)
       print "leave E"

class F(E,D,G):
    def __init__(self):
       print "enter F"
       E.__init__(self)
       # D.__init__(self)
       print "leave F"

class Class1(object):
    def __init__(self):
        print 'enter class1'
        print 'leave class1'

class Class2(Class1):
    def __init__(self):
        print 'enter class2'
        # super(Class2, self).__init__()
        print 'leave class2'

class Class3(Class2):
    def __init__(self):
        print 'enter class3'
        super(Class3, self).__init__()
        print 'leave class3'

def public_func():
    print 'public function'

def __private_fuc():
    print 'private function'


# f = F()
class3 = Class3()
'''
result:
enter F
enter E
enter B
leave B
enter C
enter A
leave A
leave C
leave E
enter D
enter A
leave A
leave D
leave F
'''

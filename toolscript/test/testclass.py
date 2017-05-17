#coding=utf-8
__author__ = 'xuxin'
#
# class A(object):
#     def func1(self):
#         print 'A: func1()'
#     def func2(self):
#         print 'A: func2()'
#
# class B(A):
#     def func1(self):
#         print 'B: func1()'
#     def func3(self):
#         print 'B: func3()'
# if __name__=='__main__':
#     object_b = B()
#     object_b.func1()
#     object_b.func2()
#     object_b.func3()

# class AA(object):
#     def __init__(self):
#         print 'A1'
#         print 'A2'
# class BB(AA):
#     def __init__(self):
#         print 'B1'
#         super(BB,self).__init__()
#         print 'B2'
# class CC(BB):
#     def __init__(self):
#         print 'C1'
#         super(CC,self).__init__()
#         print 'c2'
# # xx = CC()
# list1 = ['  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current\n', '                                 Dload  Upload   Total   Spent    Left  Speed\n', '\r  0     0    0     0    0    12      0  14652 --:--:-- --:--:-- --:--:-- 14652{"code":500,"description":"The server encountered an unexpected condition which prevented it from fulfilling the request","reasonPhrase":"Internal Server Error","throwable":{"cause":null,"stackTrace":[{"methodName":"removePool","fileName":"LoadBalancer.java","lineNumber":892,"className":"net.floodlightcontroller.loadbalancer.LoadBalancer","nativeMethod":false},{"methodName":"removePool","fileName":"PoolsResource.java","lineNumber":84,"className":"net.floodlightcontroller.loadbalancer.PoolsResource","nativeMethod":false},{"methodName":"invoke","fileName":null,"lineNumber":-1,"className":"sun.reflect.GeneratedMethodAccessor136","nativeMethod":false},{"methodName":"invoke","fileName":null,"lineNumber":-1,"className":"sun.reflect.DelegatingMethodAccessorImpl","nativeMethod":false},{"methodName":"invoke","fileName":null,"lineNumber":-1,"className":"java.lang.reflect.Method","nativeMethod":false},{"methodName":"doHandle","fileName":"ServerResource.java","lineNumber":524,"className":"org.restlet.resource.ServerResource","nativeMethod":false},{"methodName":"delete","fileName":"ServerResource.java","lineNumber":181,"className":"org.restlet.resource.ServerResource","nativeMethod":false},{"methodName":"doHandle","fileName":"ServerResource.java","lineNumber":456,"className":"org.restlet.resource.ServerResource","nativeMethod":false},{"methodName":"doNegotiatedHandle","fileName":"ServerResource.java","lineNumber":683,"className":"org.restlet.resource.ServerResource","nativeMethod":false},{"methodName":"doConditionalHandle","fileName":"ServerResource.java","lineNumber":357,"className":"org.restlet.resource.ServerResource","nativeMethod":false},{"methodName":"handle","fileName":"ServerResource.java","lineNumber":1014,"className":"org.restlet.resource.ServerResource","nativeMethod":false},{"methodName":"handle","fileName":"Finder.java","lineNumber":246,"className":"org.restlet.resource.Finder","nativeMethod":false},{"methodName":"doHandle","fileName":"Filter.java","lineNumber":159,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"handle","fileName":"Filter.java","lineNumber":206,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"doHandle","fileName":"Router.java","lineNumber":431,"className":"org.restlet.routing.Router","nativeMethod":false},{"methodName":"handle","fileName":"Router.java","lineNumber":648,"className":"org.restlet.routing.Router","nativeMethod":false},{"methodName":"doHandle","fileName":"Filter.java","lineNumber":159,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"handle","fileName":"Filter.java","lineNumber":206,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"doHandle","fileName":"Router.java","lineNumber":431,"className":"org.restlet.routing.Router","nativeMethod":false},{"methodName":"handle","fileName":"Router.java","lineNumber":648,"className":"org.restlet.routing.Router","nativeMethod":false},{"methodName":"doHandle","fileName":"Filter.java","lineNumber":159,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"handle","fileName":"Filter.java","lineNumber":206,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"doHandle","fileName":"Filter.java","lineNumber":159,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"handle","fileName":"Filter.java","lineNumber":206,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"doHandle","fileName":"Filter.java","lineNumber":159,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"handle","fileName":"Filter.java","lineNumber":206,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"doHandle","fileName":"Filter.java","lineNumber":159,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"doHandle","fileName":"StatusFilter.java","lineNumber":155,"className":"org.restlet.engine.application.StatusFilter","nativeMethod":false},{"methodName":"handle","fileName":"Filter.java","lineNumber":206,"classNam\r100  8108    0  8108    0    12  1896k   2873 --:--:-- --:--:-- --:--:-- 2635k\n', 'e":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"doHandle","fileName":"Filter.java","lineNumber":159,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"handle","fileName":"Filter.java","lineNumber":206,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"handle","fileName":"CompositeHelper.java","lineNumber":211,"className":"org.restlet.engine.CompositeHelper","nativeMethod":false},{"methodName":"handle","fileName":"ApplicationHelper.java","lineNumber":84,"className":"org.restlet.engine.application.ApplicationHelper","nativeMethod":false},{"methodName":"handle","fileName":"Application.java","lineNumber":384,"className":"org.restlet.Application","nativeMethod":false},{"methodName":"doHandle","fileName":"Filter.java","lineNumber":159,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"handle","fileName":"Filter.java","lineNumber":206,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"doHandle","fileName":"Router.java","lineNumber":431,"className":"org.restlet.routing.Router","nativeMethod":false},{"methodName":"handle","fileName":"Router.java","lineNumber":648,"className":"org.restlet.routing.Router","nativeMethod":false},{"methodName":"doHandle","fileName":"Filter.java","lineNumber":159,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"handle","fileName":"Filter.java","lineNumber":206,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"doHandle","fileName":"Router.java","lineNumber":431,"className":"org.restlet.routing.Router","nativeMethod":false},{"methodName":"handle","fileName":"Router.java","lineNumber":648,"className":"org.restlet.routing.Router","nativeMethod":false},{"methodName":"doHandle","fileName":"Filter.java","lineNumber":159,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"doHandle","fileName":"StatusFilter.java","lineNumber":155,"className":"org.restlet.engine.application.StatusFilter","nativeMethod":false},{"methodName":"handle","fileName":"Filter.java","lineNumber":206,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"doHandle","fileName":"Filter.java","lineNumber":159,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"handle","fileName":"Filter.java","lineNumber":206,"className":"org.restlet.routing.Filter","nativeMethod":false},{"methodName":"handle","fileName":"CompositeHelper.java","lineNumber":211,"className":"org.restlet.engine.CompositeHelper","nativeMethod":false},{"methodName":"handle","fileName":"Component.java","lineNumber":406,"className":"org.restlet.Component","nativeMethod":false},{"methodName":"handle","fileName":"Server.java","lineNumber":516,"className":"org.restlet.Server","nativeMethod":false},{"methodName":"handle","fileName":"ServerConnectionHelper.java","lineNumber":257,"className":"org.restlet.engine.connector.ServerConnectionHelper","nativeMethod":false},{"methodName":"doHandleInbound","fileName":"ServerConnectionHelper.java","lineNumber":186,"className":"org.restlet.engine.connector.ServerConnectionHelper","nativeMethod":false},{"methodName":"run","fileName":"BaseHelper.java","lineNumber":593,"className":"org.restlet.engine.connector.BaseHelper$2","nativeMethod":false},{"methodName":"runWorker","fileName":null,"lineNumber":-1,"className":"java.util.concurrent.ThreadPoolExecutor","nativeMethod":false},{"methodName":"run","fileName":null,"lineNumber":-1,"className":"java.util.concurrent.ThreadPoolExecutor$Worker","nativeMethod":false},{"methodName":"run","fileName":null,"lineNumber":-1,"className":"java.lang.Thread","nativeMethod":false}],"message":null,"localizedMessage":null,"suppressed":[]},"uri":"http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5.1","globalError":false,"redirection":false,"recoverableError":false,"error":true,"serverError":true,"connectorError":false,"clientError":false,"success":false,"informational":false}']
# str2 = list1[len(list1)-1]
# print str2

def spamrun(fn):
    # def sayspam(*args):
    print "spam,spam,spam"
    # print fn(*args)
    # return sayspam
@spamrun
def useful(a,b):
    print a**2+b**2

class A(object):
    name = 'A'
    def __init__(self):
        print 'Enter A'
        name = 'A2'
        print 'Leave A'

class C(A):
    name = 'C'
    def __init__(self):
        print 'Enter C'
        name = "C2"
        print 'leave C'

class B(C):
    name = 'B'
    # def __init__(self):
    #     print 'Enter B'
    #     super(B,self).__init__()  #调用父类的构造函数，只调用继承的第一个父类，super之调用上一层父类的构造函数
    #     print 'Leave B'

if __name__ == '__main__':
    # useful(3,4)
    b_obj = B()
    # print dict(B)
    print B.__dict__
    print b_obj.name
    b_obj.name = 'zhangsan'
    print b_obj.__dict__
    # pass


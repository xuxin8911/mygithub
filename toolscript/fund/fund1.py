# coding=utf-8
__author__ = 'xuxin'

RATE = 0.8

#20150318
hnpc = 20.87
ews = 17.95
nfzy = 16.85
fund = 10000

'''
1 1 3 8937.0
1 2 2 9047.0
1 3 1 9157.0
2 1 2 9339.0
2 2 1 9449.0
3 1 1 9741.0
'''

#20150319
'''
nfzy 16.60  200
hnpc 20.40  200
ewsA 17.60  100
'''

#
'''
nfzy 17.04
hnpc 21.30
ewsA 18.11
'''

def func():
    for i in xrange(1,10):
        for j in xrange(1,10):
            for k in xrange(1,10):
                fund = 100*hnpc*i + 100*ews*j + 100*nfzy*k
                if fund < 10000 and fund > 8000:
                    print i,j,k,fund

if __name__ == '__main__':
    func()

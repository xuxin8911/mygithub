# coding=utf-8
__author__ = 'xuxin'

def test_try():
    try:
        print '1'
        return '11'
    except:
        print '2'
        return '22'
    finally:
        print '3'
        # return'33'

if __name__ == '__main__':
    print test_try()
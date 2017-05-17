#coding=utf-8
__author__ = 'xuxin'


def get_role(a):
    role_list = []
    a = pow(2,a)
    for i in range(0,255):
        if a&i == a:
            role_list.append(i)
            print i
    return role_list

if __name__ == '__main__':
    a = 7
    get_role(a)


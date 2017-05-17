#coding=utf-8
__author__ = 'xuxin'

def dn_parser(dn):
    dn_list = dn.split(',')
    ou_list = []
    domain_list = []
    for i in range(len(dn_list)):
        name = dn_list[i].split('=')[0]
        value = dn_list[i].split('=')[1]
        if i == 0:
            user=value
        else:
            if name == 'DC':
                domain_list.append(value)
            else:
                ou_list.append(value)
    ou_list.reverse() #反转ou
    ou = '/'.join(ou_list)
    domain = '.'.join(domain_list)
    return user,ou,domain


if __name__ == '__main__':
    dn = "CN=Administrators,ou=Builtin,ou=test,ou=abc,DC=yongda,DC=com"
    user,ou,domain = dn_parser(dn)
    print user,ou,domain



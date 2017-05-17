__author__ = 'xuxin'
def test():
    ip_list = [['192.168.1.110','192.168.1.111'],['192.168.1.112','192.168.1.113'],
               ['192.168.1.114','192.168.1.110'],['192.168.1.110','192.168.1.115']]
    ip_dict = {}
    for i in ip_list:
        ip1,ip2 = i
        if ip1 not in ip_dict.keys():
            if ip2 not in ip_dict.keys():
                ip_dict[ip1] = [ip2,[ip1,ip2]]
            else:
                ip_dict[ip2].append([ip1,[ip1,ip2]])
        else:
            if ip2 not in ip_dict.keys():
                ip_dict[ip1].append([ip2,[ip1,ip2]])
    print ip_dict

def test2():
    beflist=[['192.168.1.110','192.168.1.111'],
    ['192.168.1.112','192.168.1.113'],
    ['192.168.1.114','192.168.1.110'],
    ['192.168.1.110','192.168.1.115']
    ]
    tmpdict={}
    for li in beflist:
        li.sort()
        if li[0] in tmpdict:
            tmpdict[li[0]].append(li[1])
        else:
            tmpdict[li[0]]=[li[1]]

    print tmpdict

def test3(a=0,b=1):
    list1 = [['a','1'],['b','2'],['c','3'],['a','5']]
    ret_list = []
    for i in list1:
        flag = 0
        for j in ret_list:
            if i[0] == j['compute_zone']:
                flag = 1
                j['compute'] = ','.join((j['compute'],i[1]))
        if flag == 0:
            ret_list.append(dict(compute_zone=i[0],compute=i[1]))
    print ret_list
    print a
    print b

def test4():
    str1 = '''+-------+------------+-----+-----------+---------+
| HOST  | PROJECT    | cpu | memory_mb | disk_gb |
+-------+------------+-----+-----------+---------+
| host1 | (total)    | 32  | 32044     | 208     |
| host1 | (used_now) | 7   | 14848     | 140     |
| host1 | (used_max) | 0   | 0         | 0       |
+-------+------------+-----+-----------+---------+
'''
    list1 = str1.rstrip().split('\n')
    for i in range(len(list1)):
        list2 = list1[i].rstrip('|').split('|')
        if i ==3:
            total_cpu,total_memory,total_disk = int(list2[3]),int(list2[4]),int(list2[5])
        elif i == 4:
            used_cpu,used_memory,used_disk = int(list2[3]),int(list2[4]),int(list2[5])
    print list1

def test5():
    host_list = [{"total_cpu": 32, "total_disk": 208, "host_state": "up", "total_memory": 32044, "used_memory": 14848,
                   "host_zone": "nova", "used_disk": 140, "used_cpu": 7, "host_name": "host1"},
                  {"total_cpu": 32, "total_disk": 208, "host_state": "down", "total_memory": 32044, "used_memory": 14848,
                   "host_zone": "nova", "used_disk": 140, "used_cpu": 7, "host_name": "host"}]
    ret_list = []
    for i in host_list:
        flag = 0
        for j in ret_list:
            if i['host_zone'] == j['host_zone']:
                flag = 1
                j['total_cpu'] = j['total_cpu'] + i['total_cpu']
                j['total_disk'] = j['total_disk'] + i['total_disk']
                j['total_memory'] = j['total_memory'] + i['total_memory']
                j['used_disk'] = j['used_disk'] + i['used_disk']
                j['used_cpu'] = j['used_cpu'] + i['used_cpu']
                j['used_memory'] = j['used_memory'] + i['used_memory']
                j['host_name'] = ','.join((j['host_name'],i['host_name']))
                if i['host_state'] == 'down' and j['host_state'] == 'down':
                    j['host_state'] = 'down'
                else:
                    j['host_state'] = 'up'
        if flag == 0:
            ret_list.append(i)
    print ret_list

if __name__ == '__main__':
    # test()
    # test2()
    # test3(b=2)
    # test4()
    test5()
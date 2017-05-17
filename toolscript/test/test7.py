#coding=utf-8
__author__ = 'xuxin'

def combList(self,List):
    '''
    合并数据，将AppID相同的项合并
    '''
    AppList = []
    retList = []
    # from pydev import pydevd
    # pydevd.settrace('192.168.1.153',port=7000,stdoutToServer=True,stderrToServer=True)
    for i in List:
        AppID = i['AppID']
        if AppID in AppList:
            for j in retList:
                if AppID == j['AppID']:
                    j['count'] = i['count'] + j['count']
                    j['eventList'].extend(i['eventList'])
                    health = int(i['health']) + int(j['health']) - 100
                    if health >= 0 :
                        j['health'] = health
                    else:
                        j['health'] = 0
                    business = (i['busy'] + j['busy'])/2
                    j['business'] = '%.2f'%business
                    for n in range(6):
                        j['riskList'][n] = i['riskList'][n] + j['riskList'][n]
        else:
            AppList.append(AppID)
            retDict = {}
            retDict['AppID'] = AppID
            retDict['AppName'] = i['AppName']
            retDict['count'] = i['count']
            retDict['eventList'] = i['eventList']
            retDict['health'] = i['health']
            retDict['busy'] = i['busy']
            retDict['riskList'] = i['riskList']
            retList.append(retDict)
    return retList

def str_to_dict(str):
    '''
    字符串转换成字典
    id=4a94318b5431482e9f17d719e647569a,user=domainname,passwd=NDNkZDVjZWMwNmNmNTMzMGJjNGVhYmVkCg==
    '''
    list1 = str.split(',')

if __name__ == '__main__':
    str1 = 'id=4a94318b5431482e9f17d719e647569a,user=domainname,passwd=NDNkZDVjZWMwNmNmNTMzMGJjNGVhYmVkCg=='
    list1 = str1.split(',')
    ret_dict = {}
    for i in list1:
        list2 = i.split('=')
        ret_dict[list2[0]] = list2[1]
    print list1
    print ret_dict
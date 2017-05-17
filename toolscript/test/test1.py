#coding:utf-8
# import time
# class A1():
#     def func1(self):
#         print 1
# class B1(A1):
#     def func2(self):
#         return 2
# time1 = time.time()
# time2 = time.localtime(time1)
# time3 = time.strftime('%Y-%m-%d %H:%M:%S',time2)
# time4 = time1 - 30
# time5 = time.localtime(time4)
# time6 = time.strftime('%Y-%m-%d %H:%M:%S',time5)
#
#
# str1 = '13971985862'
# # str1[3] = '1'
# str2 = []
# for i in range(len(str1)):
#     if i in [3,4,5,6]:
#         str2.append('*')
#     else:
#         str2.append(str1[i])
# print ''.join(str2)

list1 = [{'count':3,'AppID':29},
         {'count':4,'AppID':29},
         {'count':3,'AppID':30}]
AppList = []
retList = []
for i in list1:
    AppID = i['AppID']
    if AppID in AppList:
        for j in retList:
            if AppID == j['AppID']:
                j['count'] = i['count'] + j['count']
    else:
        AppList.append(AppID)
        retDict = {}
        retDict['AppID'] = AppID
        retDict['count'] = i['count']
        retList.append(retDict)
print retList


list1 = [{'count': 1, 'eventList': [{'eventName': 'Ping 192.168.5.10 ', 'cid': 1052, 'time': '2013/12/12 13:52:30', 'risk': 0, 'sid': 1}],
          'health': 70, 'business': 0.66, 'riskList': [1, 0, 0, 0, 0, 0],'AppID':29},
         {'count': 2, 'eventList':[{'eventName': 'Ping 192.168.5.11 ', 'cid': 1052, 'time': '2013/12/12 13:52:30', 'risk': 0, 'sid': 1}],
        'health': 60, 'business': 0.86, 'riskList': [1, 1, 0, 0, 0, 0],'AppID':29}]
AppList = []
retList = []
for i in list1:
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
                business = (i['business'] + j['business'])/2
                j['business'] = '%.2f'%business
                for n in range(6):
                    j['riskList'][n] = i['riskList'][n] + j['riskList'][n]
    else:
        AppList.append(AppID)
        retDict = {}
        retDict['AppID'] = AppID
        retDict['count'] = i['count']
        retDict['eventList'] = i['eventList']
        retDict['health'] = i['health']
        retDict['business'] = i['business']
        retDict['riskList'] = i['riskList']
        retList.append(retDict)
print retList




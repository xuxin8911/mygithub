#coding=utf-8
__author__ = 'xuxin'
List1 = [{'AppID':29,'Ip':'192.168.5.10','riskList':[5,0,0,0,0,0]},
        {'AppID':29,'Ip':'192.168.5.10','riskList':[5,2,0,0,0,0]},
        {'AppID':30,'Ip':'192.168.5.10','riskList':[5,0,0,0,0,0]},
        {'AppID':30,'Ip':'192.168.5.11','riskList':[5,0,0,1,0,0]}]
List2 = [{'AppID':29,'risk':[{'Ip':'192.168.5.10','riskList':[10,2,0,0,0,0]}]},
         {'AppID':30,'risk':[{'Ip':'192.168.5.10','riskList':[5,0,0,0,0,0]},{'Ip':'192.168.5.11','riskList':[5,0,0,1,0,0]}]}]
AppList = []
IpRiskList = []
retList = []
def func1(List1):
    for i in List1:
        retDict = {}
        if i['AppID'] in AppList:
            riskDict = {}
            for j in retList:
                if i['AppID'] == j['AppID']:
                    if i['Ip'] not in j['IpList']:
                        j['IpList'].append(i['Ip'])
        else:
            AppList.append(i['AppID'])
            retDict['AppID'] = i['AppID']
            retDict['IpList'] = []
            retDict['IpList'].append(i['Ip'])
            retList.append(retDict)
    print retList

def func2(List):
    dict1={}
    for i in range(len(List)):
        if List[i]['AppID'] in dict1.keys():
            dict1[List[i]['AppID']].append([List[i]['Ip'],List[i]['riskList']])
        else:
            dict1[List[i]['AppID']]=[[List[i]['Ip'],List[i]['riskList']]]

    templist=[]
    for k in dict1:
        dict2={}
        for i in range(len(dict1[k])):
            if dict1[k][i][0] in dict2.keys():
                for index in range(len(dict2[dict1[k][i][0]])):
                    dict2[dict1[k][i][0]][index]=dict2[dict1[k][i][0]][index]+dict1[k][i][1][index]
            else:
                dict2[dict1[k][i][0]]=dict1[k][i][1]
        templist.append([k,dict2])

    for i in range(len(templist)):
        tempdict={}
        tempdict['AppID']=templist[i][0]
        templist[i].pop(0)
        for key in templist[i][0].keys():
            tempdict[key]=templist[i][0][key]
        List2.append(tempdict)
    print List2
func1(List1)
# func2(List1)
# print retList
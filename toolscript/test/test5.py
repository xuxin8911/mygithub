__author__ = 'xuxin'
List = [{'AppID':29,'Ip':'192.168.5.10','riskList':[5,0,0,0,0,0]},
        {'AppID':29,'Ip':'192.168.5.10','riskList':[5,2,0,0,0,0]},
        {'AppID':30,'Ip':'192.168.5.10','riskList':[5,0,0,0,0,0]},
        {'AppID':30,'Ip':'192.168.5.11','riskList':[5,1,0,1,0,0]}]
relist=[]
di={}
di2={}
di3={}
for i in List:
    if i['AppID'] in di:
        if i['Ip'] in di[i['AppID']]:
            di[i['AppID']][i['Ip']] = [(lambda x,y:x+y)(di[i['AppID']][i['Ip']][j],i['riskList'][j]) for j in range(len(i['riskList']))]
        else:
            di[i['AppID']][i['Ip']]=i['riskList']
    else:
        di[i['AppID']]={}
        di[i['AppID']][i['Ip']]=i['riskList']

for i in di:
    di2['AppID']=i
    di2['risk']=[]
    for j in di[i]:
        di3['Ip']=j
        di3['riskList']=di[i][j]
        di2['risk'].append(di3)
        di3={}
    relist.append(di2)
    di2={}

print relist

#coding=utf-8
from xml.etree import ElementTree
import csv

def get_xml(file_path):
    xml_list = []
    #加载xml文件
    f = open(file_path)
    xml = f.read()
    f.close()
    xml = ''.join(['<root>',xml,'</root>'])
    root = ElementTree.fromstring(xml)
    group_name = root.attrib.get('name')
    # 获取element的方法
    xml_list = []
    group_list = root.findall('group')
    for group in group_list:
        group_name = group.attrib.get('name')
        node_list = group.findall('rule')
        for node in node_list:
            group_ret= group_name.split(',')
            if '' in group_ret:
                group_ret.remove('')
            group_name = ','.join(group_ret)
            desc = ''
            for child in node.getchildren():
                if child.tag == 'description':
                    desc = child.text
            node.attrib.update(dict(desc=desc))
            rule = node.attrib
            flag = False
            for i in xml_list:
                if group_name == i['group_name']:
                    i['rule_list'].append(rule)
                    flag = True
                    break
            if not flag:
                xml_list.append(dict(group_name=group_name,rule_list=[rule]))
    return xml_list

def write_csv(xml_list):
    csvfile = file('syslog_rules.csv','wb')
    write = csv.writer(csvfile)
    write.writerow(['group_name','rule_id','level','desc'])
    for i in xml_list:
        for j in i['rule_list']:
            write.writerow((i['group_name'],j['id'],j['level'],j['desc']))
    csvfile.close()




if __name__ == "__main__":
    file_path = 'syslog_rules.xml'
    xml_list = get_xml(file_path)
    write_csv(xml_list)
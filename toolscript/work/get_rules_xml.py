#coding=utf-8
__author__ = 'xuxin'
from xml.etree import ElementTree
import os,StringIO
import MySQLdb

'''
编写脚本解析ossec产生的事件xml文件，将数据存储到事件信息表中
plugin_sid
/var/ossec/rules
rule id
description
level
plugin_group_descr
plugin_group
group
步骤：1、获取文件列表
      2、读取xml文件
      3、提取信息存储到事件信息表
'''
dir = '/var/ossec/rules'
def get_file_list():
    file_list = os.listdir(dir)
    print len(file_list)
    for file in file_list:
        filepath = '/'.join([dir,file])
        #判断是否是文件
        if not os.path.isfile(filepath):
            file_list.remove(file)
            continue
        #判断是否是xml文件
        if file[-4:] != '.xml':
            file_list.remove(file)
    print len(file_list)
    return file_list

def get_xml(file_list):
    xml_list = []
    for file in file_list:
        # file = 'rules_config.xml'
        filepath = '/'.join([dir,file])

        #加载xml文件
        f = open(filepath)
        xml = f.read()
        f.close()
        xml = ''.join(['<root>',xml,'</root>'])
        root = ElementTree.fromstring(xml)
        group_name = root.attrib.get('name')
        # 获取element的方法
        group_list = root.findall('group')
        for group in group_list:
            group_name = group.attrib.get('name')
            node_list = group.findall('rule')
            for node in node_list:
                xml_dict = {}
                group_list = group_name.split(',')
                if '' in group_list:
                    group_list.remove('')
                xml_dict['group_list'] = group_list
                desc = ''
                for child in node.getchildren():
                    if child.tag == 'description':
                        desc = child.text
                xml_dict['desc'] = desc
                for i in node.items():
                    xml_dict[i[0]] = i[1]
                xml_list.append(xml_dict)
    return xml_list

def connect():
    host = '127.0.0.1'
    user = 'root'
    passwd = '12345678'
    db = 'ssoc'
    port = 3307
    conn = MySQLdb.connect(host,user,passwd,db,port)
    return conn

def insert_record(xml_dict):
    group_list = xml_dict['group_list']
    id = xml_dict['id']
    level = int(xml_dict['level'])/3
    desc = xml_dict['desc']
    for group in group_list:
        conn = connect()
        curs = conn.cursor()
        #判断是否有分组，有分组用已有的groupid,没分组添加分组并用生成的groupid
        sql1 = "select group_id from plugin_group_descr where name='%s'"%group
        curs.execute(sql1)
        result = curs.fetchall()
        count_id = len(result)
        if count_id > 0:
            group_id = result[0][0]
        else:
            #添加组
            sql2 = "insert into plugin_group_descr(name,descr) values('%s','%s')"%(group,group)
            curs.execute(sql2)
            conn.commit()
            sql3 = "select last_insert_id()"
            curs.execute(sql3)
            result2 = curs.fetchall()
            group_id = result2[0][0]
        plugin_id = 7007
        #添加事件
        sql8 = "select count(sid) from plugin_sid where plugin_id='%s' and sid='%s'"%(plugin_id,id)
        curs.execute(sql8)
        result = curs.fetchall()
        count = result[0][0]
        if count > 0:
            continue
        desc = desc.replace('"',"'")
        ARO = 0
        sql4 = '''insert into plugin_sid(plugin_id,sid,priority,name,ARO) values("%s","%s","%s","%s","%s")'''%(plugin_id,id,level,desc,ARO)
        try:
            curs.execute(sql4)
            conn.commit()
        except:
            print sql4

        sql5 = "select plugin_sid from plugin_group where group_id='%s'and plugin_id='%s'"%(group_id,plugin_id)
        curs.execute(sql5)
        result = curs.fetchall()
        if len(result) > 0:#记录存在
            plugin_sid = result[0][0]
            plugin_sid_list = plugin_sid.split(',')
            if id not in plugin_sid:
                plugin_sid = ','.join([plugin_sid,id])
                sql6 = "update plugin_group set plugin_sid='%s' where group_id=%s and plugin_id=%s"%(plugin_sid,group_id,plugin_id)
                curs.execute(sql6)
                conn.commit()
        else:
            plugin_sid = id
            sql7 = "insert into plugin_group(group_id,plugin_id,plugin_sid) values('%s','%s','%s')"%(group_id,plugin_id,plugin_sid)
            curs.execute(sql7)
            conn.commit()

if __name__ == '__main__':
    file_list = get_file_list()
    xml_list = get_xml(file_list)
    for xml in xml_list:
        insert_record(xml)
    print '------ success ------'
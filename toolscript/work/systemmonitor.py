#coding=utf-8
__author__ = 'Administrator'

import ConfigParser
import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from Products.ZenModel.DeviceClass import DeviceClass

def system_print():
    print '**********************************************************'
    print '*********         0、退出监控配置               ***********'
    print '*********         1、主机监控                   ***********'
    print '*********         2、数据库监控                 ***********'
    print '*********         3、web监控                   ***********'
    print '**********************************************************'

def host_print():
    print '**********************************************************'
    print '*********         0、退出主机监控配置           ***********'
    print '*********         1、Windows系统               ***********'
    print '*********         2、Linux系统                 ***********'
    print '**********************************************************'

def windows_host_print():
    print '**********************************************************'
    print '*********         0、退出Windows主机监控配置    ***********'
    print '*********         1、WMI                       ***********'
    print '*********         2、SNMP                      ***********'
    print '**********************************************************'

def linux_host_print():
    print '**********************************************************'
    print '*********         0、退出Linux主机监控配置      ***********'
    print '*********         1、SNMP                      ***********'
    print '*********         2、cmd                       ***********'
    print '**********************************************************'

def host_monitor():
    while True:
        host_print()
        host_input = input('请输入要监控的主机类型编号：')
        if host_input == 0:
            print '退出主机监控'
            break
        elif host_input == 1:
            windows_host_print()
            windows_host_input = input('请注入windows主机监控方式:')
            if windows_host_input == 0:
                print '退出windows主机监控!'
                break
            elif windows_host_input == 1:
                print 'WMI监控，请先配置WMI'
            elif windows_host_input == 2:
                print 'SNMP监控，请先配置SNMP'
            else:
                print '输入错误!'
                continue
        elif host_input == 2:
            linux_host_print()
        else:
            print '输入错误!'
            continue

def database_monitor():
    print '数据库监控配置'

def web_monitor():
    print 'web监控配置'

def run():
    print '开始系统监控配置...'
    while True:
        system_print()
        system_input = input('请输入要监控的系统类型编号：')
        if system_input == 0:
            print '退出系统!'
            break
        elif system_input == 1:
            host_monitor()
        elif system_input == 2:
            database_monitor()
        elif system_input == 3:
            web_monitor()
        else:
            print '输入错误!'
            continue


class SetMonitor(ZenScriptBase):
    '''
    设置监控模板
    '''
    def setBondTemplates(self,ip,new_templateIds):
        '''
        绑定监控模板
        :param ip:IP地址
        :param new_templateIds:新增监控模板  ['MySQLSSH']
        :return:
        '''
        self.connect()
        obj = self.dmd.Devices.findDevice(ip)
        templateIds = obj.zDeviceTemplates
        for i in new_templateIds:
            if i not in templateIds:
                templateIds.append(i)
        result = obj.bindTemplates(templateIds)
        return result

    def copyTemplate(self, uid, targetUid):
        '''
        本地化监控模板
        :param uid:"/zport/dmd/Devices/rrdTemplates/MySQLSSH"
        :param targetUid:"/zport/dmd/Devices/Server/SSH/Linux/devices/172.168.10.14"
        :return:
        '''
        template = self._getTemplate(uid)
        target = self._getObject(targetUid)
        marker = object()
        source = getattr(template, 'device', marker)
        if source is marker and isinstance(target, DeviceClass):
            # copying to and from a DeviceClass
            source = template.deviceClass()
            source.manage_copyAndPasteRRDTemplates((template.id,), targetUid)
        else:
            if isinstance(target, DeviceClass):
                # copying from a Device to a DeviceClass
                container = target.rrdTemplates
            else:
                # copying from either to a Device
                container = target
            if template.id in container.objectIds():
                msg = '"%s" already contains template "%s".'
                args = (targetUid, template.id)
                raise Exception(msg % args)
            copy = template._getCopy(container)
            container._setObject(copy.id, copy)

    def setZenProperty(self, ip, zProperty, value):
        '''
        设置设备属性
        :param ip:IP地址
        :param zProperty:设备属性 zCommandPort
        :param value:属性值  22
        :return:
        '''
        self.connect()
        obj = self.dmd.Devices.findDevice(ip)
        ztype = obj.getPropertyType(zProperty)
        if ztype == 'int':
            value = int(value)
        if ztype == 'float':
            value = float(value)
        if ztype == 'string':
            value = str(value)
        # do not save * as passwords
        if obj.zenPropIsPassword(zProperty) and value == obj.zenPropertyString(zProperty):
            return
        return obj.setZenProperty(zProperty, value)

    def setInfo(self, uid, data):
        '''
        设置监控模板属性
        :param uid::"/zport/dmd/Devices/Server/SSH/Linux/devices/172.168.10.14/MySQLSSH/datasources/mysqlssh"
        :param data:{"cycletime":30,"eventKey":"123421"}
        :return:
        '''
        obj = self._getObject(uid)
        info = self._getDataSourceInfoFromObject(obj)
        newId = None
        if 'newId' in data:
            newId = data['newId']
            del data['newId']
            info.rename(newId)

        for key in data.keys():
            if hasattr(info, key):
                setattr(info, key, data[key])
        return info

if __name__ == '__main__':
    Monitor = SetMonitor()
    from pydev import pydevd
    pydevd.settrace('192.168.1.153',port=7000,stdoutToServer=True,stderrToServer=True)
    ip = '172.168.10.10'
    zProperty = 'zCommandPort'
    value = '22'
    Monitor.setZenProperty(ip,zProperty,value)

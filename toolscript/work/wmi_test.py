__author__ = 'Administrator'
import wmi
connection = wmi.connect_server(server='172.168.10.242',user='administrator',
				password='12')
WMI = wmi.GetObject('winmgmts:')
# sql1 = 'SELECT DiskReadsPerSec,DiskWritesPerSec FROM Win32_PerfRawData_PerfDisk_PhysicalDisk WHERE Name="_Total"'
# result =  WMI.ExecQuery(sql1)

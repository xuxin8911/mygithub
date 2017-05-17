#coding:utf-8
__author__ = 'Administrator'
import os,sys,time
import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase

class ActionCmd(ZenScriptBase):
	action_map = {"dolibvirtReboot":"重启",
			   "dolibvirtSave":"备份",
			   "dolibvirtResume":"恢复",
			   "dolibvirtSuspend":"挂起",
			   "dolibvirtStartup":"启动",
			   "dolibvirtShutdown":"关机",
			   "dolibvirtDestroy":"强制关机"}

	def run(self):
		try:
			t1= time.time()
			self.connect()
			if self.action_map.has_key(self.options.action):
				dev = self.dmd.Devices.findDeviceByIdOrIp(self.options.devid)
			if dev is None:
				print "没找到设备"
				return
			if dev.deviceClass().id == "VirtDevice":
				g = dev.virtguest()
				if getattr(g,self.options.action)():
					t2 = time.time()
					self.sendEvent("/Repair",self.options.devid,"修复云主机成功",1,"修复：%s云主机%s结果：成功, 共耗时：%.2f秒"%(self.action_map[self.options.action],dev.manageIp,t2-t1))
				else:
					self.sendEvent("/Repair",self.options.devid,"修复云主机失败",2,"修复：%s云主机%s结果：失败, 共耗时：%.2f秒"%(self.action_map[self.options.action],dev.manageIp,t2-t1))
			else:
				self.sendEvent("/Repair",self.options.devid,"修复云主机失败",2,"修复：%s云主机%s结果：失败,不支持该操作, 共耗时：0秒"%(self.action_map[self.options.action],dev.manageIp))
		except:
			import traceback
			print traceback.print_exc()
			self.sendEvent("/Repair",self.options.devid,"修复云主机失败",2,"修复：%s云主机%s异常"% (self.action_map[self.options.action],dev.manageIp))

	def buildOptions(self):
		self.parser.add_option('--devid',
							   dest='devid',
							   default=None,
							   help="device ip or id")
		self.parser.add_option('--action',
							   dest='action',
							   default=None,
							   help="exec action")
		ZenScriptBase.buildOptions(self)


	def sendEvent(self,eventClass,dev,summary,severity,message):
		eventDict = {
			'eventClass': eventClass,
			'device': dev,
			'summary': summary,
			'severity': severity,
			'message': message
			}
		self.dmd.ZenEventManager.sendEvent(eventDict)

if __name__=="__main__":
	a = ActionCmd()
	a.run()

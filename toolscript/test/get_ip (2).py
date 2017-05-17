#coding=utf-8
__author__ = 'xuxin'
import logging,Globals,sys
from Products.ZenUtils.Ext import DirectRouter, DirectResponse
from Products import Zuul
from Products.Zuul.decorators import require

import AccessControl

log = logging.getLogger('zen.ZenPackRouter')
class UMRouter(DirectRouter):

    def _getFacade(self):
        return Zuul.getFacade('um', self.context)

    def get_user_ip(self):
        dmd = self._getFacade()._getDmd()
	


if __name__ == '__main__':
    print sys.argv[0]
    print sys.argv[1]
    print sys.argv[2]
    pass

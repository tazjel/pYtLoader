# -*- coding: utf-8 -*-

import time
import modules.cfg

#simple logger :-)
class log:
	def __init__(self):
			pass
			
	def start(self):
		print "================"
		print time.strftime("%d. %b %Y %H:%M:%S", time.localtime())
		print _("%s-v%s started") %(modules.cfg.name, modules.cfg.version)


	def info(self, text):
		print _("%s %s") %(time.strftime("[%H:%M:%S]", time.localtime()),text)
	
	def error(self, text):
		print _("%s ERROR: %s") %(time.strftime("[%H:%M:%S]", time.localtime()),text)

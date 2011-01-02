# -*- coding: utf-8 -*-

import wx
#EVENT
modules.cfg.wxEVT_THREAD_COM = wx.NewEventType()
class ThreadEvent(wx.PyEvent):
	def __init__(self, pfad, title):
		wx.PyEvent.__init__(self)
		self.SetEventType(modules.cfg.wxEVT_THREAD_COM)
		self.pfad = pfad
		self.title = title
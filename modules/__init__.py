# -*- coding: utf-8 -*-

import cfg
try:
	import wx
except ImportError:
	cfg.iswx = False
	
from engine import Youtube
from log import log
from ID3 import *

if cfg.iswx:
	from gui import gui
	from gui import ThreadEvent
	from gui import tagger
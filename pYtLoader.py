#!/usr/bin/env python2
# -*- coding: utf-8 -*-
######################
#v93ytLoader-v2.6
######################
#v93.eu#
######################
#Lizens, Haftung, Anleitung
#siehe Liesmich.txt
######################
#short 1080p clip (no webm -.-)
#http://www.youtube.com/watch?v=fGTMirS6L_c
######################
#TOBO:id3tag: "http://img.youtube.com/vi/"..video_id.."/default.jpg"
#engine:Array(fmt,resoltuion,url)
import urllib,webbrowser,os,tempfile,time,threading,re, sys
import gettext
from optparse import OptionParser
from optparse import OptionGroup
import modules
import modules.cfg

trans = gettext.translation("v93ytLoader", "locale", ["de"]) 
trans.install(unicode=True)


#leerzeile
print ""
#Die ganzen Argumente wenn man diese Datei auf der shell verwendet (z.B. ohne X-server)
parser = OptionParser()
parser.usage = "%prog [options] YouTubeUrl [YTUrl] ..."
parser.description = _("This is a easy program to download YouTube videos and extract the audio to mp3. (with shell or gui) (for mp3 lame and faad2 is required)")
parser.epilog = _("This program is biodegradable.")

group = OptionGroup(parser, _("Normal options"), _("Example for a fullHD-download and mp3 conversion:\n'YouTubeDownloader -c --fullhd http://www.youtube.com/watch?v=uxk4hIX3Kn4'."))
advanced_group = OptionGroup(parser, _("advanced options"), _("Options, for non normal people."))
group.add_option("-c", "--convert", dest="convert", help=_("Convert video to (can be used only with mp4)."), default=False, action="store_true")
group.add_option("", "--hd", dest="usehd", help=_("Download in high quality (720p), if available."), default=False, action="store_true")
group.add_option("", "--fullhd", dest="usefullhd", help=_("Download in high quality (1080p), if available."), default=False, action="store_true")
group.add_option("-3", "--3gp", dest="use3gp", help=_("Download as 3gp for mobile phones video (MPEG-4)."), default=False, action="store_true")
group.add_option("-l", "--flv", dest="useflv", help=_("Download video as flv."), default=False, action="store_true")
advanced_group.add_option("-f", "--fmt", dest="usefmt", help=_("Download video in custom quality (-f 0 to show the fmt list; Without this option the best quality will be downloaded.)"), metavar="FMT")
advanced_group.add_option("", "--megahd", dest="usemegahd", help=_("Download in very high quality (4096x2304), if available."), default=False, action="store_true")
advanced_group.add_option("", "--3gp4", dest="use3gp4", help=_("Download as 3gp for mobile phones video (h263)."), default=False, action="store_true")
advanced_group.add_option("-w", "--webm", dest="usewebm", help=_("Download video in WebM."), default=False, action="store_true")
advanced_group.add_option("-u", "--url", dest="useurl", help=_("Only print download URL."), default=False, action="store_true")
advanced_group.add_option("-b", "--webbrowser", dest="useweb", help=_("Open downloadurl in your default webbrowser. (senseless?!)"), default=False, action="store_true")
parser.add_option_group(group)
parser.add_option_group(advanced_group)
(options, args) = parser.parse_args()

if not options.usefmt:
	#12345678901 da das mit einer hohen Wahrscheinlichkeit  nicht als fmt genommen wird, aber usefmt dann weder None 0 oder ein andere int sein darf, sonst gibts Probleme :)
	usefmt = 12345678901
	bestqual = True
else: 	
	usefmt = int(options.usefmt)
	bestqual = False
usehd =  options.usehd
usefullhd =  options.usefullhd
usemegahd =  options.usemegahd
use3gp = options.use3gp
use3gp4 = options.use3gp4
useflv = options.useflv
convert = options.convert
useurl = options.useurl
useweb = options.useweb
usewebm = options.usewebm



if  (usefmt == 0):
	print _("mp4 - fmt-list")
	print _("FMT = Resolution")
	print "%3.0f = %s" % ( 18, "480x270   /(default)")
	print "%3.0f = %s" % ( 22, "1280x720  /--hd")
	print "%3.0f = %s" % ( 34, "854x480")
	print "%3.0f = %s" % ( 35, "854x480")
	print "%3.0f = %s" % ( 36, "320x240")
	print "%3.0f = %s" % ( 37, "1920x1080 /--fullhd")
	print "%3.0f = %s" % ( 38, "4096x2304 /--megahd")
	print "%3.0f = %s" % ( 40, "426x240")
	print 
	print _("For more infos see fmt.xls")
	quit()

modules.log().start()
modules.log().info(_("logging the world"))

#Wo bin ich gerade?
if sys.platform == "win32":
	modules.cfg.iswin = True
	modules.log().info(_("We are on a Windows Operating System"))
else:
	modules.log().info(_("THIS IS LINUX!!! (or similar)"))

gui_enabled = False

if modules.cfg.iswin:
	windows_size_x = 395
	windows_size_y = 235
else:
	windows_size_x = 455
	windows_size_y = 200

#UserAgent andern, Da YouTube = Google --> mag keine Bots auf seinen Webseiten
class UserAgent(urllib.FancyURLopener):
	version = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.8) Gecko/20100214 Ubuntu/9.10 (karmic) Firefox/3.5.8'
urllib._urlopener = UserAgent()





#http://www.youtube.com/watch?v=47DlwB6Ih2s


if __name__=='__main__':
	#wenn die Datei mit argumenten aufgerufen wird nicht die gui starten sondern gleich downloaden
	if (usefmt == '0') or  args:
		#~ print args

		c= modules.Youtube(args,usehd,usefullhd,use3gp,useflv,convert,useweb, useurl, usewebm, usefmt,bestqual)
		#~ c= modules.Youtube(args,frame,usehd,usefullhd,use3gp,useflv,convert,useweb)
		c.start()
		
	#ohne aurgumente --> gui starten
	else:
		try:
			import wx
		except ImportError:
			modules.cfg.iswx = False
			#von shell starten
			modules.log().info(_("No wx-widgets found."))

		
		if modules.cfg.iswx:
			import modules.gui
			app=wx.PySimpleApp()
			modules.cfg.frame=modules.gui(None,-1, windows_size_x, windows_size_y, modules.Youtube)
			modules.cfg.frame.Center()
			modules.cfg.frame.SetMinSize((windows_size_x,windows_size_y))
			modules.cfg.frame.Show()
			app.MainLoop()
			#~ from modules.event import ThreadEvent
	

		

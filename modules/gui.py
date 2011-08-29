# -*- coding: utf-8 -*-

import re, wx, time, os, ConfigParser
import modules.log
import modules.cfg
import modules.ID3


class CustomStatusBar(wx.StatusBar):
	def __init__(self, parent):
		wx.StatusBar.__init__(self, parent, -1)
		self.SetFieldsCount(1)

#EVENT
class ThreadEvent(wx.PyEvent):
	def __init__(self, pfad, title):
		wx.PyEvent.__init__(self)
		self.SetEventType(modules.cfg.wxEVT_THREAD_COM)
		self.pfad = pfad
		self.title = title

class tagger(wx.MiniFrame):
	def __init__(self, parent, id, pfad, title):
		modules.log().info(_("Starting Tagger" ))
		self.title = title
		self.pfad = pfad
		self.autofill = True

		wx.Frame.__init__(self, parent, id, "Tagger - " + self.title, style = wx.DEFAULT_MINIFRAME_STYLE)

		self.panel_tagger = wx.Panel(self)

		#Buttons
		self.CButton_tagger = wx.Button(self.panel_tagger, -1, _("Close"), size=(70,35))
		self.Bind(wx.EVT_BUTTON, self.doClose, self.CButton_tagger)
		self.AFButton_tagger = wx.Button(self.panel_tagger, -1, _("AutoFill"), size=(70,35))
		self.Bind(wx.EVT_BUTTON, self.doAutoFill, self.AFButton_tagger)

		#Text
		self.Text_Titel_tagger = wx.StaticText(self.panel_tagger, -1, _("Titel:"), )
		self.Text_Album_tagger = wx.StaticText(self.panel_tagger, -1, _("Album:"))
		self.Text_Interpret_tagger =  wx.StaticText(self.panel_tagger, -1, _("Interpret:"))

		#Box
		self.Titel_tagger = wx.TextCtrl(self.panel_tagger, -1, "", style=wx.TE_CENTRE|wx.TE_PROCESS_ENTER)
		self.Album_tagger = wx.TextCtrl(self.panel_tagger, -1, "", style=wx.TE_CENTRE|wx.TE_PROCESS_ENTER)
		self.Interpret_tagger = wx.TextCtrl(self.panel_tagger, -1, "", style=wx.TE_CENTRE|wx.TE_PROCESS_ENTER)

		#ToolTips
		self.Titel_tagger.SetToolTipString(_("The titel of the song."))
		self.Album_tagger.SetToolTipString(_("The Album, on witch this song ws published."))
		self.Interpret_tagger.SetToolTipString(_("The band/The singer/The DJ who \nhas published this Song on a album."))

		#Sizer
		self.Grid_Sizer_tagger = wx.GridSizer(4, 2, 5, 0)
		self.Grid_Sizer_tagger.Add(self.Text_Titel_tagger, 0, wx.ALIGN_RIGHT|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 10)
		self.Grid_Sizer_tagger.Add(self.Titel_tagger, 0,  wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
		self.Grid_Sizer_tagger.Add(self.Text_Album_tagger, 0, wx.ALIGN_RIGHT|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 10)
		self.Grid_Sizer_tagger.Add(self.Album_tagger, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
		self.Grid_Sizer_tagger.Add(self.Text_Interpret_tagger, 0, wx.ALIGN_RIGHT|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 10)
		self.Grid_Sizer_tagger.Add(self.Interpret_tagger, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
		self.Grid_Sizer_tagger.Add(self.CButton_tagger, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
		self.Grid_Sizer_tagger.Add(self.AFButton_tagger, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)

		self.panel_tagger.SetSizer(self.Grid_Sizer_tagger)
		self.Grid_Sizer_tagger.Fit(self)

	def doClose(self, event):
		#Die ID3tags schreiben
		modules.log().info(_("Set id3-tag"))
		self.id3info = modules.ID3(self.pfad)
		self.id3info['TITLE'] = self.Titel_tagger.GetValue()
		self.id3info['ARTIST'] = self.Interpret_tagger.GetValue()
		self.id3info['ALBUM'] = self.Album_tagger.GetValue()
		print self.id3info
		self.Destroy()

	def doAutoFill(self, event):
		self.title_split = self.title.split(" - ")
		if self.autofill:
			self.Interpret_tagger.SetValue(self.title_split[0])
			self.title_split.pop(0)
			self.Titel_tagger.SetValue(str(self.title_split).replace("', '", " - ").replace("['", "").replace("']", ""))
			self.autofill = False
		else:
			self.Titel_tagger.SetValue(self.title_split[0])
			self.title_split.pop(0)
			self.Interpret_tagger.SetValue(str(self.title_split).replace("', '", " - ").replace("['", "").replace("']", ""))
			self.autofill = True

class gui(wx.Frame):
	def __init__(self, parent, id, _Youtube):
		self.Youtube = _Youtube
		wx.Frame.__init__(self, parent, id, "%s %s" %(modules.cfg.name, modules.cfg.version), size = (modules.cfg.windows_size_x, modules.cfg.windows_size_y))
		self.panel = wx.Panel(self)
		self.showAdvancedWindow = False

		#Custom, da sonst in Windows alles verrutscht ist
		self.sb = CustomStatusBar(self.panel)
#EVENT
		self.Connect(-1, -1, modules.cfg.wxEVT_THREAD_COM, self.OnThreadCommunicationEvent)
#EVENT

	#DAS ADVANCED FENSTER -->
		self.win = wx.MiniFrame(self, -1, _("Advanced"), wx.Point(100,100) , size = (modules.cfg.windows_size_x_win, modules.cfg.windows_size_y_win), style = wx.DEFAULT_MINIFRAME_STYLE)
		self.win.Show(False)

		self.panel_win = wx.Panel(self.win)
		self.CButton_win = wx.Button(self.panel_win, -1, _("Close"), size = (70, 35))
		self.Bind(wx.EVT_BUTTON, self.doHide, self.CButton_win)
		self.RegexBox_win = wx.CheckBox (self.panel_win, -1, _('Check YouTube-Urls.'))
		self.Advancedfmt_win = wx.CheckBox ( self.panel_win, -1, _('More resolutions'))
		self.Bind(wx.EVT_CHECKBOX, self.doDType, self.Advancedfmt_win)
		self.Tagger_win = wx.CheckBox ( self.panel_win, -1, _('Activate mp3-Tagger. (BETA)'))
		self.Bind(wx.EVT_CHECKBOX, self.doTagger, self.Tagger_win)
		self.Font_win = wx.CheckBox ( self.panel_win, -1, _('Enable "Comic Sans MS" as Font'))
		self.Bind(wx.EVT_CHECKBOX, self.doFont, self.Font_win)

		#Language
		self.mylist = ['Deutsch', 'English']
		self.LanguageList_win = wx.ListBox(self.panel_win, -1, (-1, -1), (120, 60), self.mylist, wx.LB_SINGLE)
		self.LanguageList_win.SetSelection(0)
		self.Bind(wx.EVT_LISTBOX, self.doLanguageBox, self.LanguageList_win)

		#Positionierung mit sizers
		self.Checkbox_win = wx.BoxSizer(wx.VERTICAL)
		self.Checkbox_win.Add(self.RegexBox_win, 0, wx.ALL, border = 5)
		self.Checkbox_win.Add(self.Advancedfmt_win, 0, wx.ALL, border = 5)
		self.Checkbox_win.Add(self.Tagger_win, 0, wx.ALL, border = 5)
		self.Checkbox_win.Add(self.Font_win, 0, wx.ALL, border = 5)
		self.Checkbox_win.Add(self.LanguageList_win, 0, wx.ALL, border = 5)
		self.Checkbox_win.Add(self.CButton_win, 0, wx.LEFT, border = 10)

		self.Advanced_win = wx.BoxSizer()
		self.Advanced_win.Add(self.Checkbox_win, 0, wx.ALL, border = 5)
		self.panel_win.SetSizer(self.Advanced_win)
		#<--DAS ADVANCED FENSTER 

		#Schriftgroese und art deffinieren 
		self.font1 = wx.Font(19, wx.SWISS, wx.ITALIC, wx.NORMAL, False)
		self.font2 = wx.Font(17, wx.SWISS, wx.NORMAL, wx.BOLD, False)
		self.font3 = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL, False)

		#DIE EIGENTLICHE GUI-->

		#Der Text ueber dem Textfeld und das Textfeld
		self.UrlText = wx.StaticText(self.panel, -1, _("Youtube Urls (seperated with spaces):"))
		self.Url = wx.TextCtrl(self.panel, -1, "", style = wx.TE_PROCESS_ENTER)
		self.Url.SetFont(self.font1)
		self.Url.SetFocus()
		#Dass wenn man ENTER drueckt der Download startet
		self.Bind(wx.EVT_TEXT_ENTER, self.doDownload, self.Url)

		#Gauge (ProcessBar :D) ##wx.GA_HORIZONTAL
		self.Gauge = wx.Gauge(self.panel, -1, 100, size = (20, 165), style = wx.GA_VERTICAL)

		#Checklist
		self.mylist = ['.flv', '.3gp', '.mp4', '.mp4 (720p)', '.mp4 (1080p)', '(.webm)']
		self.DType = wx.ListBox(self.panel, -1, (-1, -1), (120, 60), self.mylist, wx.LB_SINGLE)
		self.DType.SetSelection(3)
		self.Bind(wx.EVT_LISTBOX, self.doListBox, self.DType)

		#Advanced-Button
		self.ConvertBox = wx.CheckBox ( self.panel, -1, _('Convert to mp3'))
		self.AdvancedBox = wx.Button ( self.panel, -1, _('Advanced'))
		self.Bind(wx.EVT_BUTTON, self.doAdvanced, self.AdvancedBox)

		#Dieverse Knoepfe+was sie passiert wenn sie gedrueckt werden
		self.DButton = wx.Button(self.panel, -1, _("Download"), size = (140, 80))
		self.DButton.SetFont(self.font2)
		self.Bind(wx.EVT_BUTTON, self.doDownload, self.DButton)		
		self.RButton = wx.Button(self.panel, -1, _("Reset"), size = (70, 35))
		self.RButton.SetFont(self.font3)
		self.Bind(wx.EVT_BUTTON, self.doReset, self.RButton)		
		self.CButton = wx.Button(self.panel, -1, _("Close"), size = (70, 35))
		self.CButton.SetFont(self.font3)
		self.Bind(wx.EVT_BUTTON, self.doClose, self.CButton)

		#SIZER (Positionierung der Elemente)
		#mySizer.Add(thing, proportion, flag(s), border, userData)

		#Reset/Close Buttons
		self.Button = wx.BoxSizer(wx.VERTICAL)
		self.Button.Add(self.RButton, 0, wx.ALL, border = 5)
		self.Button.Add(self.CButton, 0, wx.ALL, border = 5)

		#CheckList+CheckBox
		self.Check = wx.BoxSizer(wx.VERTICAL)
		self.Check.Add(self.ConvertBox, 0, wx.TOP, border = -7)
		self.Check.Add(self.DType, 1, wx.ALL|wx.EXPAND, border = 5)

		#List+DownloadButton
		self.Bottom = wx.BoxSizer()
		self.Bottom.Add(self.Check, 1, wx.ALL|wx.EXPAND, border = 5)
		self.Bottom.Add(self.DButton, 1, wx.ALL, border = 5)
		self.Bottom.Add(self.Button, 0, wx.ALL|wx.EXPAND, border = 0)

		#Die Uberschrift und die Advancedcheckbox
		self.Top = wx.BoxSizer()
		self.Top.Add(self.UrlText, 0, wx.TOP|wx.LEFT, border = 5)
		self.Top.Add(self.AdvancedBox, 0, wx.LEFT, border = 50)

		#Schrift+Eingababebox(goesenveraenderbar)
		self.UrlBox = wx.BoxSizer(wx.VERTICAL)
		self.UrlBox.Add(self.Top, 0, wx.TOP|wx.LEFT, border = 5)
		self.UrlBox.Add(self.Url, 0, wx.ALL|wx.EXPAND, border = 5)
		self.UrlBox.Add(self.Bottom, 1, wx.EXPAND|wx.ALL, border = 0)

		#Gauge
		self.MainSizer = wx.BoxSizer()
		self.MainSizer.Add(self.UrlBox, 1, wx.EXPAND|wx.ALL, border = 0)
		self.MainSizer.Add(self.Gauge, 0, wx.EXPAND|wx.RIGHT|wx.TOP|wx.BOTTOM, border = 5)

		#StatusBar
		self.SBSizer = wx.BoxSizer(wx.VERTICAL)
		self.SBSizer.Add(self.MainSizer, 1, wx.ALL|wx.EXPAND, border = 5)
		self.SBSizer.Add(self.sb, 0, wx.EXPAND, border = 0)

		self.panel.SetSizer(self.SBSizer)

	#alles zuruecksetzen
	def doReset(self, event):
		self.DType.SetSelection(3)
		self.Url.SetValue("")
		self.Url.SetFocus()
		self.ConvertBox.SetValue(0)
		self.ConvertBox.Enable(True)

	#Wenn 3gp, webm oder flv wird die Convert Checkbox ausgegraut und Deaktiviert
	def doListBox(self, event):
		if (not self.Advancedfmt_win.GetValue() and ((self.DType.GetSelection() < 2) or (self.DType.GetSelection() == 5))) or (self.Advancedfmt_win.GetValue() and self.DType.GetSelection() < 5):
			self.ConvertBox.SetValue(False)
			self.ConvertBox.Enable(False)
		else:
			self.ConvertBox.Enable(True)

	def doClose(self, event):
		self.Destroy()

	def doHide(self, event):
		self.win.Show(False)
		self.showAdvancedWindow = False
		self.writeConfigFile()

	def writeConfigFile(self):
		config = ConfigParser.RawConfigParser()
		config.add_section("Advanced")
		config.set("Advanced", "regex", self.RegexBox_win.GetValue())
		config.set("Advanced", "advanced_fmt", self.Advancedfmt_win.GetValue())
		config.set("Advanced", "tagger", self.Tagger_win.GetValue())
		config.set("Advanced", "comic_font", self.Font_win.GetValue())
		config.set("Advanced", "language", self.LanguageList_win.GetSelection()) #TODO: Nicht die Nummer sondern Sprachcode speichern

		with open('pYtLoader.ini', 'wb') as configfile:
			config.write(configfile)

	def readConfigFile(self):
		config = ConfigParser.RawConfigParser()
		config.read('pYtLoader.ini')
		try:
			self.RegexBox_win.SetValue(config.getboolean("Advanced", "regex"))
			self.Advancedfmt_win.SetValue(config.getboolean("Advanced", "advanced_fmt"))
			self.Tagger_win.SetValue(config.getboolean("Advanced", "tagger"))
			self.Font_win.SetValue(config.getboolean("Advanced", "comic_font"))
			self.LanguageList_win.SetSelection(config.getboolean("Advanced", "language"))
		except ConfigParser.NoSectionError:
			modules.log().info(_("Could not find a correct config file."))
		except ConfigParser.NoOptionError:
			modules.log().info(_("Some options in the config file are incorrect."))
		except:
			modules.log().info(_("Unexpected error by reading the config file."))
		else:
			self.doDType(None)
			self.doFont(None)
			self.doLanguageBox(None)

	def doAdvanced(self, event):
		if self.showAdvancedWindow:
			self.win.Show(False)
			self.showAdvancedWindow = False
			self.writeConfigFile()
		else:
			self.win.Show(True)
			self.showAdvancedWindow = True


	def doDownload(self, event):
		if self.Url.GetValue() == "":
			self.sb.SetStatusText(_("Please enter YouTube-Url(s) in the textbox."))
		else:
			self.usehd =  False
			self.usefullhd =  False
			self.usemegahd =  False
			self.use3gp = False
			self.useflv = False
			self.convert = False
			self.useweb =  False
			self.useurl =  False
			self.usewebm =  False
			self.usefmt =  False
			self.bestqual = False

			#Wenn der haken gesetzt ist...
			if self.Advancedfmt_win.GetValue():
				if self.DType.GetSelection() == 0:
					self.useflv =True
				elif self.DType.GetSelection() == 1:
					self.use3gp = True
				elif self.DType.GetSelection() == 3:
					#normales webm
					self.usewebm = True
				elif self.DType.GetSelection() == 4:
					#HD webm
					self.usewebm = True
					self.usehd = True
				elif self.DType.GetSelection() == 5:
					#das mit 0.8fps :D
					self.usefmt = 40
				elif self.DType.GetSelection() == 6:
					self.usefmt = 36
				elif self.DType.GetSelection() == 7:
					#Default mp4 fmt18
					#self.usefmt = 18
					pass
				elif self.DType.GetSelection() == 8:
					#mp4 640x360
					self.usefmt = 34
				elif self.DType.GetSelection() == 9:
					#mp4 854x480
					self.usefmt = 35
				elif self.DType.GetSelection() == 10:
					self.usehd = True
				elif self.DType.GetSelection() == 11:
					self.usefullhd = True
				elif self.DType.GetSelection() == 12:
					self.usemegahd = True
			else:
				#Was wurde in der ListBox ausgewaehlt
				if self.DType.GetSelection() == 0:
					self.useflv =True
				elif self.DType.GetSelection() == 1:
					self.use3gp = True
				elif self.DType.GetSelection() == 3:
					self.usehd = True
				elif self.DType.GetSelection() == 4:
					self.usefullhd = True
				elif self.DType.GetSelection() == 5:
					self.usewebm = True

			#Checkbox aktiviert
			if self.ConvertBox.GetValue():
				self.convert = True

			#Die Urls aus der Textboxauslesen und als Liste in eine Variable schreiben
			args = self.Url.GetValue().split(' ')
			self.args = args

			if self.RegexBox_win.GetValue():
				self.doRegex()
			else:
				#Den eigentlichen Download starten
				c = self.Youtube(self.args, self.usehd,self.usefullhd,self.use3gp,self.useflv,self.convert,self.useweb, self.useurl, self.usewebm, self.usefmt, self.bestqual)
				c.start()

				#die Box leeren
				self.Url.SetValue("")
				self.Url.SetFocus()

	def doRegex(self):
		#Die Urls auf YoutubeUrls prufen
		self.rg = re.compile('http:\\/\\/www\\.youtube\\.com\\/watch\\?v=[0-9 a-z A-Z _-]{11,}', re.IGNORECASE|re.DOTALL)
		self.q = 0
		self.u = 0
		for reg in self.args:			
			self.m = self.rg.match(reg)
			self.u = self.u +1
			if self.m:
				modules.log().info("'" + reg + "' is eine YouTubeUrl")
				self.q = self.q + 1
			else:
				modules.log().info( "'" + reg + "' is NOT a YouTubeUrl")

		if self.q == self.u:
			#Den eigentlichen Download starten
			c = self.Youtube(self.args, self.usehd, self.usefullhd, self.use3gp, self.useflv, self.convert, self.useweb, self.useurl, self.usewebm, self.usefmt, self.bestqual)
			c.start()

			self.Url.SetValue("")
			self.Url.SetFocus()
		else:
			self.Url.SetFocus()
			self.sb.SetStatusText(_("One or more Urls are incorrect."))

	def doDType(self,event):
		if self.Advancedfmt_win.GetValue():
			# 5 mal das erste element loeschen 
			for d in range(0, 6):
				self.DType.Delete(0)

			self.InsertList=['.flv (320x180)', '.3gp (174x144)', '.3gp (174x144)', '.(webm (640x360))', '.(webm (1280x720))', '.mp4 (426x240)', '.mp4 (480x270)', '.mp4 (640x360)', '.mp4 (854x480)', '.mp4 (1280x720)', '.mp4 (1920x1080)', '.mp4 (4096x2304)']
			self.DType.InsertItems(self.InsertList, 0)
		else:
			for d in range(0, 12):
				self.DType.Delete(0)
			self.DType.InsertItems(self.mylist, 0)

	def doTagger(self, event):
		if modules.cfg.TaggerBox == True:
			modules.cfg.TaggerBox = False
		else: 
			modules.cfg.TaggerBox = True
			self.ConvertBox.SetValue(1)
			self.ConvertBox.Enable(True)
			#doListBox um zu uberprufen ob man das videoformat wirklich konvertieren kann,
			#wenn nicht --> wirds wieder ausgegraut und SetValue(0) 
			self.doListBox(None)

	def doFont(self, event):
		if self.Font_win.GetValue():
			#Schriftgroese und Art deffinieren #NiX
			self.font1 = wx.Font(19, wx.SWISS, wx.ITALIC, wx.NORMAL, False)
			self.font2 = wx.Font(17, wx.SWISS, wx.NORMAL, wx.BOLD, False)
			self.font3 = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL, False)
		else:
			#Schriftgroese und Art deffinieren #Comic Sans MS
			self.font1 = wx.Font(19, wx.SWISS, wx.ITALIC, wx.NORMAL, False, u'Comic Sans MS')
			self.font2 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD, False, u'Comic Sans MS')
			self.font3 = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')

		self.Url.SetFont(self.font1)
		self.DButton.SetFont(self.font2)
		self.RButton.SetFont(self.font3)
		self.CButton.SetFont(self.font3)

	def doLanguageBox(self, event):
		if hasattr(modules.language, 'myLocal'):
			del modules.language.myLocal

		if (self.LanguageList_win.GetSelection() == 0):
			modules.language.myLocal = wx.Locale(wx.LANGUAGE_GERMAN, wx.LOCALE_LOAD_DEFAULT | wx.LOCALE_CONV_ENCODING)
		else:
			modules.language.myLocal = wx.Locale(wx.LANGUAGE_ENGLISH_US, wx.LOCALE_LOAD_DEFAULT | wx.LOCALE_CONV_ENCODING)

		modules.language.myLocal.AddCatalog('pYtLoader')
		modules.language.setLanguage()

	#Wenn event  kommt das taggerfenster starten, mit event.* werden nochtitel und pfad ubergeben.
	def OnThreadCommunicationEvent(self, event):
		self.pfad = event.pfad
		self.title = event.title
		#Tagger
		App_tagger = wx.PySimpleApp()
		Frame_tagger = modules.tagger(None, -1, self.pfad, self.title)
		Frame_tagger.Center()
		Frame_tagger.Show()
		App_tagger.MainLoop()
		event.Skip()
# -*- coding: utf-8 -*-


import urllib,webbrowser,os,tempfile,time,threading,sys
import modules.cfg
import modules.log

#~ import modules.tagger
try:
	import wx
	#~ from modules.event import ThreadEvent
except ImportError:
	modules.log().info(_("No wx-widgets found. (engine)"))


class Youtube(threading.Thread):
	def __init__(self, args,usehd,usefullhd,use3gp,useflv,convert,useweb, useurl, usewebm, usefmt,bestqual):
	#~ def __init__(self,frame,args,usehd,usefullhd,use3gp,useflv,convert,useweb):
		threading.Thread.__init__(self)        
		self.args=args
		self.usehd=usehd
		self.usefullhd=usefullhd
		self.use3gp=use3gp
		self.useflv=useflv
		self.convert=convert
		self.useweb=useweb
		self.useurl = useurl
		self.usewebm=usewebm
		self.usefmt = usefmt
		self.bestqual = bestqual
		
	def run(self):
		
		modules.log().info('----------------')
		
		
		if modules.cfg.iswin:
			#Ordner falls nicht vorhanden anlegen
			self.home = os.environ["HOMEPATH"] + '\\Eigene Dateien'
			if not os.path.exists(self.home + "\\YouTube") :
				os.mkdir(self.home + "\\YouTube")
			if not os.path.exists(self.home + "\\YouTube\\mp4") :
				os.mkdir(self.home + "\\YouTube\\mp4")
			if not os.path.exists(self.home + "\\YouTube\\mp3") :
				os.mkdir(self.home + "\\YouTube\\mp3")
			if not os.path.exists(self.home + "\\YouTube\\3gp") :
				os.mkdir(self.home + "\\YouTube\\3gp")
			if not os.path.exists(self.home + "\\YouTube\\flv") :
				os.mkdir(self.home + "\\YouTube\\flv")
			if not os.path.exists(self.home + "\\YouTube\\webm") :
				os.mkdir(self.home + "\\YouTube\\webm")
		else:
			self.home = os.environ["HOME"]
			#Ordner falls nicht vorhanden anlegen
			if not os.path.exists(self.home + "/YouTube") :
				os.mkdir(self.home + "/YouTube")
				modules.log().info(_(' ~/Youtube/ directory and subdirectories created.'))
			if not os.path.exists(self.home + "/YouTube/mp4") :
				os.mkdir(self.home + "/YouTube/mp4")
			if not os.path.exists(self.home + "/YouTube/mp3") :
				os.mkdir(self.home + "/YouTube/mp3")
			if not os.path.exists(self.home + "/YouTube/3gp") :
				os.mkdir(self.home + "/YouTube/3gp")
			if not os.path.exists(self.home + "/YouTube/webm") :
				os.mkdir(self.home + "/YouTube/webm")
		
		for video in self.args :
			#Quelltext herunterladen und einzeln auslesen
			modules.log().info(_('Download and parse Sourcecode...'))
			h = urllib.urlopen(video)
			modules.log().info(_('...downloaded...'))
			for line in h.readlines():
				#Die Linie mit der javascript variable "swfHTML" in eine Variable schreiben
				if line.find("'PLAYER_CONFIG':") != -1:
					swfArgs = line
				#Den Titel  finden und aus dem Quelltext 'extrahieren'
				if line.find("<meta name=\"title\" content=\"") != -1:
					self.title = line.replace("<meta name=\"title\" content=\"", "").replace("\">", "").strip()
			
			self.title = self.title.replace(":", " ")
			self.title = self.title.replace("|", " ")
			self.title = self.title.replace("\\", " ")
			self.title = self.title.replace("/", " ")
			
			
			#NOW USELESS!!! (I think...)
			#die video_id finden und speichern
			for lol in swfArgs.split(',') :
				if lol.find('video_id') != -1:
					video_id = lol
			video_id = video_id.split('"')[-2]
			#~ print video_id


			#NOW USELESS!!! (I think...)
			#die geheimnissvolle "t"(oken) Variable finden und speichern
			for lol in swfArgs.split(',') :
				if lol.find('"t":') != -1:
					t = lol
			t = t.split('"')[-2]
			#~ print t
			
			
			fmt_map_all=[] # [[fmt][resolution][url]][...]
			fmt_map_all_sub = []
			fmt_map_resolution = []
			
			#Verfuegbare Formate finden
			for lol in swfArgs.split(', "') :
				if lol.find('fmt_map":') != -1:
					fmt_map_pre = lol
			fmt_map_pre = fmt_map_pre.split('"')[-2]
			
			
			#Verfuegbare fmts und Download Formate finden
			for lol in swfArgs.split(', "') :
				if lol.find('fmt_url_map":') != -1:
					fmt_url_map_pre = lol
			fmt_url_map_pre = fmt_url_map_pre.split('"')[-2]
			
			#wieviele Auflosungen vorhanden sind
			rescount = fmt_map_pre.count(',') +1
			
			#verfuegbare Auflosungen finden 
			for lol in fmt_map_pre.split(','):
				fmt_map_resolution.append(lol.split('\\/')[1])
			
			#verfuegbare fmts und Download urls finden finden 
			i = 0
			for lol in fmt_url_map_pre.split(','):
				fmt_map_all_sub = []
				fmt_map_all_sub.append(int(lol.split('|')[0]))
				fmt_map_all_sub.append(fmt_map_resolution[i])
				fmt_map_all_sub.append((lol.split('|')[1]).replace("\/", "/").replace("\u0026","&"))
				
				fmt_map_all.append(fmt_map_all_sub)
				i = i +1
			
			#~ modules.log().info(("Debug ausgabe: %s") %fmt_url_map_url[2][0])
			

			modules.log().info(_("Resolutions: %d (Best: %s).") %(rescount,fmt_map_all[0][1]))

			
			isHDAvailable = False
			isFullHDAvailable = False
			isMegaHDAvailable = False
			
			for i in range(len(fmt_map_all)):
				#pruefen ob 720p HD verfuegbar ist 
				if fmt_map_all[i][0] == 22:
					isHDAvailable = True
				#pruefen ob 1080p HD verfuegbar ist
				if fmt_map_all[i][0] == 37:
					isFullHDAvailable = True
				#pruefen ob megahd/orginal? verfuegbar ist
				if fmt_map_all[i][0] == 38:
					isMegaHDAvailabe = True
				#~ quit()
			


	
			modules.log().info(_('...parsed.'))
			
			#Schauen als was heruntergeladen werden soll und "fmt" und Endung 
			#anpassen sonst als normale mp4 herunterladen
			fmt = 18
			self.suffix = ".mp4"
			
	
			if self.usefmt != False and self.usefmt != 12345678901:
				fmt = self.usefmt
				modules.log().info(_("Use custom fmt=%s.") %fmt)
				#~ print self.usefmt
				if self.usefmt == 5:
					self.suffix = ".flv"
				elif self.usefmt == 17 or self.usefmt == 13:
					self.suffix = ".3gp"
				elif self.usefmt == 18 or self.usefmt == 22 or self.usefmt == 34 or self.usefmt == 35 or self.usefmt == 36 or self.usefmt == 37 or self.usefmt == 38 or self.usefmt == 40:
					self.suffix = ".mp4"
				elif self.usefmt == 43 or self.usefmt == 45:
					self.suffix = ".webm"
				else:
					self.suffix = ""
	
			
			if self.useflv :
				fmt = 5
				self.suffix = ".flv"
			elif self.use3gp :
				fmt = 17
				self.suffix = ".3gp" 
			elif self.usehd :
				if self.usewebm:
					fmt = 45
				else:
					if isHDAvailable:
							fmt = 22
					else :
						modules.log().info(_("Video is not in HD(720p) available."))
						modules.log().info(_("Video will be downloaded in default quality."))
			elif self.usefullhd :
				if self.usewebm:
					fmt = 45 #??<--stimmt noch nicht !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
				else:
					if isFullHDAvailable:
						fmt = 37
					else :
						#Falls 1080p HD nicht ferfuegbar ist dann in 720p herunterladen und falls 
						if isHDAvailable:
							fmt = 22
							modules.log().info(_("Video is not in Full-HD(1080p) available."))
							modules.log().info(_("Video will be downloaded in HD(720p)."))				
						#das auch nicht, dann in normalem mp4
						else:
							modules.log().info(_("Video is neither in Full-HD(1080p) nor in HD(720p) available."))
							modules.log().info(_("Video will be downloaded in default quality."))
			elif self.usewebm : 
				fmt = 43
				self.suffix = ".webm" 

			#Richtiges Speicher-Verzeichniss ohne den Punkt waehlen
			if modules.cfg.iswin:
				self.dir =  self.home + '\\YouTube\\' + self.suffix[1:]
			else:
				self.dir =  self.home + '/YouTube/' + self.suffix[1:]
			
			#fmt mit fmt_url_map_url[i][0] vergleichen und dann die Download url fmt_url_map_url[i][1] nehmen.
			#Beste Qualitat?
			if self.bestqual:
				self.url = fmt_map_all[0][2]
			else:
				for i in range(len(fmt_map_all)):
					if fmt_map_all[i][0] == fmt:
						self.url = fmt_map_all[i][2]
					print fmt_map_all[i][0]
					
			
			
			#~ self.url = "http://www.youtube.com/get_video?&video_id=" + video_id + "&t=" + t  + "&asv=&fmt=%s" %fmt
			#~ print self.url
			if modules.cfg.iswin:
				#Tempfiles erstellen
				tmp_vid = tempfile.mkstemp(prefix="ytvid_", suffix=self.suffix)[1]
				tmp_wav = tempfile.mkstemp(prefix="ytwav_", suffix=".wav")[1]
				modules.log().info(_("Temp-files created."))
			
			else:
				#Tempfile erstellen
				tmp = tempfile.mkstemp(prefix="ytvid_", suffix=self.suffix)[1]
				modules.log().info(_("Temp-file created."))
			
			if self.useweb and not self.convert and not self.useurl:        
				webbrowser.open(self.url)
			elif   self.useurl and not self.useweb and not self.convert:
				print self.url
				#~ print "LLLLOOOOOOLLL"
			elif self.useweb and self.convert :
				#~ modules.log().info("Das Video kann nicht im Webbrowser geoeffnet und konvertiert werden. (Script entweder ohne -w/--webbrowser oder -c/--convert aufrufen)")
				modules.log().info(_("The Video can't opened in the browser and converted. (Use only w/--webbrowser or -c/--convert)."))
			else :
				#Die datei in die tmp-Datei Speichern
				#~ os.system('wget "' + url + '" -U "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.2) Gecko/20090804 Shiretoko/3.5.2" -O ' + tmp)	
				pass


#X
				if modules.cfg.iswin:
					urllib.urlretrieve(self.url, tmp_vid, reporthook=self.dlProgress)
				else:
					urllib.urlretrieve(self.url, tmp, reporthook=self.dlProgress)
					#~ pass
				modules.log().info(_('Download completed.'))
				

				#mit faad und lame zu mp3 convertieren
				if self.convert and not (self.use3gp or self.useflv or self.useweb)  :
					modules.log().info(_('Audiofile will be extracted.'))
					if modules.cfg.frame:
						wx.CallAfter(self.TextAfter, _("Converting..."))
					if modules.cfg.iswin:
						self.pfad = self.home + '\\YouTube\\mp3\\' + self.title + '.mp3'
						os.system('data\\faad.exe -o ' + tmp_wav + ' "' + tmp_vid + '"')
						os.system('data\\lame.exe "' + tmp_wav + '" --tc Youtube "' + self.pfad)
					else:
						self.pfad =  self.home + '/YouTube/mp3/' + self.title + '.mp3'
						os.system('faad -o - ' + tmp + ' | lame - --tc Youtube "' + self.pfad + '"')
						
					if modules.cfg.TaggerBox and modules.cfg.frame and modules.cfg.iswx:
						
						
				#EVENT
						myThreadEvent = modules.ThreadEvent(self.pfad, self.title)
						modules.cfg.frame.GetEventHandler().AddPendingEvent(myThreadEvent)	
				#EVENT
						
						
					if modules.cfg.frame:
						wx.CallAfter(self.TextAfter, _("Converted!"))
				elif self.convert :
					modules.log().info(_("Only *.mp4 can be converted."))
				#Falls Datei schon vorhanden ein teil den Unix-Timestamps als Dateinamen drannhaengen

				if os.path.isfile(self.dir + '\\' + self.title + self.suffix) :
					timestamp = str(time.time())[0:10]
					if modules.cfg.iswin:
						os.system('copy ' + tmp_vid + ' "' + self.dir + '\\' + self.title + "_new" + timestamp + self.suffix + '"')
					else:
						os.system('mv ' + tmp + ' "' + self.dir + '/' + self.title + "_new" + timestamp + self.suffix + '"')
					modules.log().info(_("Video already exists."))
					modules.log().info(_('Video will be moved to "%s/%s_new%s%s".') %(self.dir,self.title, timestamp,self.suffix))
				#Wenn noch nicht vorhanden die Tmp-Datei in das Speicher-Verzeichniss copieren und in den Tiitel des
				#Videos umbenennen
				else:
					if modules.cfg.iswin:
						os.system('copy "' + tmp_vid + '" "' + self.dir + '\\' + self.title + self.suffix + '"')
						# print 'copy "' + tmp_vid + '" "' + self.dir + '\\' + title + self.suffix + '"'
					else:
						os.system('mv ' + tmp + ' "' + self.dir + '/' + self.title + self.suffix + '"')
					modules.log().info(_('"%s" moved to %s.') %(self.title,self.dir))
					


					
					
	def dlProgress(self,count, blockSize, totalSize):
		#Wenn das Video keine groese hat ist es nicht da :-)
		#z.B http://www.youtube.com/watch?v=oIHBUGvAUMo
		#Emi Musics koennte hier schuld sein, dass es nicht in mp4 vorhanden ist.
		if totalSize == 0:
			modules.log().error(_('Video in your requested filetype not available.'))
			modules.log().error(_('Please use an other filetype.'))
			modules.log().error(_('e.g. use *.flv instead of *.mp4.'))
			if modules.cfg.frame:
				wx.CallAfter(self.TextAfter, _("ERROR: Format not available."))
			quit()
		else:
			percent = int(count*blockSize*100/totalSize)
			if modules.cfg.frame:
				wx.CallAfter(self.DlAfter, percent)
			else:
				sys.stdout.write("%2d%%" % percent)
				sys.stdout.write("\b\b\b")
				sys.stdout.flush()

		
	def DlAfter(self,percent):
		if percent == 100:
			modules.cfg.frame.Gauge.SetValue(0)
			modules.cfg.frame.sb.SetStatusText(_('Download comleted. :-)'))
			sys.stdout.write("%2d%%" % 100)
			sys.stdout.write("\b\b\b")
			sys.stdout.flush()
		else:
			
			modules.cfg.frame.Gauge.SetValue(percent)
			modules.cfg.frame.sb.SetStatusText('Downloading... ' + str(percent) + '%')
			sys.stdout.write("%2d%%" % percent)
			sys.stdout.write("\b\b\b")
			sys.stdout.flush()
			
	def TextAfter(self,text):
		modules.cfg.frame.sb.SetStatusText(text)
		

#EVENT
#~ class ThreadEvent(wx.PyEvent):
	#~ def __init__(self, pfad, title):
		#~ wx.PyEvent.__init__(self)
		#~ self.SetEventType(modules.cfg.wxEVT_THREAD_COM)
		#~ self.pfad = pfad
		#~ self.title = title
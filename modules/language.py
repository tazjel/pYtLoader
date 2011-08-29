# -*- coding: utf-8 -*-

import os, sys
import locale
import modules.cfg

if modules.cfg.iswx:
	#beim import geladene Einstellungen (für die on-the-fly Übersetzung)
	import wx
	provider = wx.SimpleHelpProvider()
	wx.HelpProvider_Set(provider)

	import __builtin__
	__builtin__.__dict__['_'] = wx.GetTranslation
	__builtin__._ = wx.GetTranslation

	wx.Locale_AddCatalogLookupPathPrefix('./locale')
	locale.setlocale(locale.LC_ALL, '')

	localVar = wx.Locale(wx.LANGUAGE_DEFAULT, wx.LOCALE_LOAD_DEFAULT | wx.LOCALE_CONV_ENCODING)
	localVar.AddCatalog('pYtLoader')
else:
	import gettext
	trans_de = gettext.translation("pYtLoader", "locale", ["de"]) 
	trans_en = gettext.translation("pYtLoader", "locale", ["en"]) 
	trans_de.install(unicode=True)


def setLanguage():
	f = modules.cfg.frame
	# Tagger noch ohne on-the-fly Übersetzung 
	#~ f.CButton_tagger.SetLabel(_("Close"))
	#~ f.AFButton_tagger.SetLabel(_("AutoFill"))
	#~ f.Text_Titel_tagger.SetLabel(_("Titel:"))
	#~ f.Text_Album_tagger.SetLabel(_("Album:"))
	#~ f.Text_Interpret_tagger.SetLabel(_("Interpret:"))

	#~ f.Titel_tagger.SetToolTipString(_("The titel of the song."))
	#~ f.Album_tagger.SetToolTipString(_("The Album, on witch this song ws published."))
	#~ f.Interpret_tagger.SetToolTipString(_("The band/The singer/The DJ who \nhas published this Song on a album."))

	f.CButton_win.SetLabel(_("Close"))
	f.RegexBox_win.SetLabel(_('Check YouTube-Urls.'))
	f.Advancedfmt_win.SetLabel(_('More resolutions'))
	f.Tagger_win.SetLabel(_('Activate mp3-Tagger. (BETA)'))
	f.Font_win.SetLabel(_('Enable "Comic Sans MS" as Font'))

	f.UrlText.SetLabel( _("Youtube Urls (seperated with spaces):"))
	f.ConvertBox.SetLabel(_('Convert to mp3'))
	f.AdvancedBox.SetLabel(_('Advanced'))
	f.DButton.SetLabel(_("Download"))
	f.RButton.SetLabel(_("Reset"))
	f.CButton.SetLabel(_("Close"))
#!/usr/bin/env python3

# This file is part of OpenPlotter.
# Copyright (C) 2022 by Sailoog <https://github.com/openplotter/openplotter-settings>
#                  
# Openplotter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# any later version.
# Openplotter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Openplotter. If not, see <http://www.gnu.org/licenses/>.

import wx, os, webbrowser, subprocess, sys, time
import wx.richtext as rt

from .conf import Conf
from .language import Language
from .platform import Platform
from .version import version
from .appsList import AppsList
from .gpio import GpioMap

class MyFrame(wx.Frame):
	def __init__(self):
		self.conf = Conf()
		self.home = self.conf.home
		self.platform = Platform()
		self.currentdir = os.path.dirname(os.path.abspath(__file__))
		currentLanguage = self.conf.get('GENERAL', 'lang')
		self.language = Language(self.currentdir,'openplotter-settings',currentLanguage)
		appsList = AppsList()
		self.appsDict = appsList.appsDict

		wx.Frame.__init__(self, None, title=_('Settings')+' '+version, size=(800,444))
		self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		icon = wx.Icon(self.currentdir+"/data/openplotter-settings.png", wx.BITMAP_TYPE_PNG)
		self.SetIcon(icon)
		self.CreateStatusBar()
		font_statusBar = self.GetStatusBar().GetFont()
		font_statusBar.SetWeight(wx.BOLD)
		self.GetStatusBar().SetFont(font_statusBar)

		self.toolbar1 = wx.ToolBar(self, style=wx.TB_TEXT)
		toolHelp = self.toolbar1.AddTool(101, _('Help'), wx.Bitmap(self.currentdir+"/data/help.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolHelp, toolHelp)
		if not self.platform.isInstalled('openplotter-doc'): self.toolbar1.EnableTool(101,False)
		else:self.toolbar1.EnableTool(101,True)
		self.toolbar1.AddSeparator()
		toolStartup = self.toolbar1.AddCheckTool(102, _('Autostart'), wx.Bitmap(self.currentdir+"/data/autostart.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolStartup, toolStartup)
		if os.path.exists(self.home+'/.config/autostart/openplotter-startup.desktop'): self.toolbar1.ToggleTool(102,True)
		self.toolbar1.AddSeparator()	
		toolCheck = self.toolbar1.AddTool(103, _('Check System'), wx.Bitmap(self.currentdir+"/data/check.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolCheck, toolCheck)
		
		self.notebook = wx.Notebook(self)
		self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onTabChange)
		self.apps = wx.Panel(self.notebook)
		self.genSettings = wx.Panel(self.notebook)
		self.raspSettings = wx.Panel(self.notebook)
		self.log = wx.Panel(self.notebook)
		self.output = wx.Panel(self.notebook)
		self.notebook.AddPage(self.apps, _('OpenPlotter Apps'))
		self.notebook.AddPage(self.genSettings, _('General Settings'))
		self.notebook.AddPage(self.raspSettings, _('Raspberry Settings'))
		self.notebook.AddPage(self.log, _('System log'))
		self.notebook.AddPage(self.output, '')

		self.il = wx.ImageList(24, 24)
		img0 = self.il.Add(wx.Bitmap(self.currentdir+"/data/openplotter-24.png", wx.BITMAP_TYPE_PNG))
		img1 = self.il.Add(wx.Bitmap(self.currentdir+"/data/debian.png", wx.BITMAP_TYPE_PNG))
		img2 = self.il.Add(wx.Bitmap(self.currentdir+"/data/rpi.png", wx.BITMAP_TYPE_PNG))
		img3 = self.il.Add(wx.Bitmap(self.currentdir+"/data/log.png", wx.BITMAP_TYPE_PNG))
		img4 = self.il.Add(wx.Bitmap(self.currentdir+"/data/output.png", wx.BITMAP_TYPE_PNG))
		self.notebook.AssignImageList(self.il)
		self.notebook.SetPageImage(0, img0)
		self.notebook.SetPageImage(1, img1)
		self.notebook.SetPageImage(2, img2)
		self.notebook.SetPageImage(3, img3)
		self.notebook.SetPageImage(4, img4)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.toolbar1, 0, wx.EXPAND)
		vbox.Add(self.notebook, 1, wx.EXPAND)
		self.SetSizer(vbox)

		self.pageGeneral()
		self.pageRpi()
		self.pageOutput()
		self.pageLog()
		self.pageApps()
		self.onListAppsDeselected()

		self.Centre()

	def ShowStatusBar(self, w_msg, colour):
		self.GetStatusBar().SetForegroundColour(colour)
		self.SetStatusText(w_msg)

	def ShowStatusBarRED(self, w_msg):
		self.ShowStatusBar(w_msg, (130,0,0))

	def ShowStatusBarGREEN(self, w_msg):
		self.ShowStatusBar(w_msg, (0,130,0))

	def ShowStatusBarBLACK(self, w_msg):
		self.ShowStatusBar(w_msg, wx.BLACK) 

	def ShowStatusBarYELLOW(self, w_msg):
		self.ShowStatusBar(w_msg,(255,140,0))

	def onTabChange(self, event):
		try:
			self.SetStatusText('')
		except:pass

	def OnToolHelp(self, event): 
		url = "/usr/share/openplotter-doc/settings/settings_app.html"
		webbrowser.open(url, new=2)

	def OnToolTranslate(self, event): 
		url = "https://crowdin.com/project/openplotter"
		webbrowser.open(url, new=2)

	def OnToolLanguage(self, event): 
		short = 'en'
		name = self.languageList.GetValue()
		for i in self.language.available:
			if name == i[0]: short = i[1]
		self.conf.set('GENERAL', 'lang', short)
		wx.MessageBox(_('Close and open again the window to see changes.'), _('Info'), wx.OK | wx.ICON_INFORMATION)

	###################################################################################

	def pageGeneral(self):
		self.toolbar3 = wx.ToolBar(self.genSettings, style=wx.TB_TEXT)
		langList = []
		for i in self.language.available:
			langList.append(i[0])
		self.languageList = wx.ComboBox(self.toolbar3, 301, _('Language'), choices=langList, size=(150,-1), style=wx.CB_DROPDOWN)
		toolLanguage = self.toolbar3.AddControl(self.languageList)
		self.Bind(wx.EVT_COMBOBOX, self.OnToolLanguage, toolLanguage)
		toolTranslate = self.toolbar3.AddTool(302, _('Translate'), wx.Bitmap(self.currentdir+"/data/crowdin.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolTranslate, toolTranslate)
		self.toolbar3.AddSeparator()
		toolMaxi = self.toolbar3.AddCheckTool(303, _('Maximize OpenPlotter Apps'), wx.Bitmap(self.currentdir+"/data/resize.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolMaxi, toolMaxi)
		self.toolbar3.AddSeparator()

		toolRescue = self.toolbar3.AddCheckTool(304, _('Rescue'), wx.Bitmap(self.currentdir+"/data/rescue.png"))
		self.Bind(wx.EVT_TOOL, self.onToolRescue, toolRescue)
		if self.conf.get('GENERAL', 'rescue') == 'yes': self.toolbar3.ToggleTool(304,True)


		starupLabel = wx.StaticText(self.genSettings, label=_('Startup'))
		self.toolbar4 = wx.ToolBar(self.genSettings, style=wx.TB_TEXT)
		toolDelay = self.toolbar4.AddCheckTool(401, _('Delay (seconds)'), wx.Bitmap(self.currentdir+"/data/delay.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolDelay, toolDelay)
		self.delay = wx.TextCtrl(self.toolbar4, 402)
		tooldelay = self.toolbar4.AddControl(self.delay)
		self.toolbar4.AddSeparator()
		toolPlay = self.toolbar4.AddCheckTool(403, _('Play'), wx.Bitmap(self.currentdir+"/data/play.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolPlay, toolPlay)
		self.pathFile = wx.TextCtrl(self.toolbar4, 404, size=(350,-1))
		toolPathFile = self.toolbar4.AddControl(self.pathFile)
		toolFile = self.toolbar4.AddTool(405, '', wx.Bitmap(self.currentdir+"/data/file.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolFile, toolFile)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.toolbar3, 0, wx.EXPAND, 0)
		sizer.Add(starupLabel, 0, wx.ALL | wx.EXPAND, 10)
		sizer.Add(self.toolbar4, 0, wx.EXPAND, 0)
		self.genSettings.SetSizer(sizer)

		maxi = self.conf.get('GENERAL', 'maximize')
		if maxi == '1': 
			self.toolbar3.ToggleTool(303,True)
			self.Maximize()

		delay = self.conf.get('GENERAL', 'delay')
		if delay:
			self.delay.SetValue(delay)
			self.delay.Disable()
			self.toolbar4.ToggleTool(401,True)

		path = self.conf.get('GENERAL', 'play')
		if not path == '':
			self.pathFile.SetValue(path)
			self.toolbar4.ToggleTool(403,True)
		else: self.pathFile.SetValue('/usr/share/sounds/openplotter/Store_Door_Chime.mp3')

	def OnToolFile(self,e):
		dlg = wx.FileDialog(self, message=_('Choose a file'), defaultDir='/usr/share/sounds/openplotter', defaultFile='',
							wildcard=_('Audio files') + ' (*.mp3)|*.mp3|' + _('All files') + ' (*.*)|*.*',
							style=wx.FD_OPEN | wx.FD_CHANGE_DIR)
		if dlg.ShowModal() == wx.ID_OK:
			file_path = dlg.GetPath()
			self.pathFile.SetValue(file_path)
			self.OnToolPlay()
		dlg.Destroy()

	def OnToolPlay(self,e=0):
		if self.toolbar4.GetToolState(403):
			path = self.pathFile.GetValue()
			if path:
				self.conf.set('GENERAL', 'play', path)
				self.ShowStatusBarGREEN(_('Sound to play at startup set to: ')+path)
			else: self.toolbar4.ToggleTool(403,False)
		else:
			self.conf.set('GENERAL', 'play', '')
			self.ShowStatusBarGREEN(_('Removed sound to play at startup'))

	def OnToolDelay(self,e):
		if self.toolbar4.GetToolState(401):
			delay = self.delay.GetValue()
			if delay:
				self.conf.set('GENERAL', 'delay', delay)
				self.ShowStatusBarGREEN(_('Delay at startup set to: ')+delay)
				self.delay.Disable()
			else: self.toolbar4.ToggleTool(401,False)
		else:
			self.conf.set('GENERAL', 'delay', '')
			self.ShowStatusBarGREEN(_('Removed delay at startup'))
			self.delay.SetValue('')
			self.delay.Enable()

	def OnToolMaxi(self,e):
		if self.toolbar3.GetToolState(303):
			self.conf.set('GENERAL', 'maximize', '1')
			self.ShowStatusBarGREEN(_('OpenPlotter apps will open maximized'))
		else:
			self.conf.set('GENERAL', 'maximize', '0')
			self.ShowStatusBarGREEN(_('Disabled maximized OpenPlotter apps'))

	def onToolRescue(self,e=0):
		if self.toolbar3.GetToolState(304): self.conf.set('GENERAL', 'rescue', 'yes')
		else: self.conf.set('GENERAL', 'rescue', 'no')

	###################################################################################

	def pageLog(self):
		self.toolbar7 = wx.ToolBar(self.log, style=wx.TB_TEXT)
		toolDebug = self.toolbar7.AddCheckTool(701, _('Debugging mode'), wx.Bitmap(self.currentdir+"/data/bug.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolDebug, toolDebug)
		self.toolbar7.AddSeparator()
		toolSeeAll= self.toolbar7.AddTool(702, _('See all'), wx.Bitmap(self.currentdir+"/data/logsee.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolSeeAll, toolSeeAll)
		toolSeeCat = self.toolbar7.AddTool(703, _('See category'), wx.Bitmap(self.currentdir+"/data/logcategory.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolSeeCat, toolSeeCat)
		toolLogSearch = self.toolbar7.AddTool(705, _('Search'), wx.Bitmap(self.currentdir+"/data/logsearch.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolLogSearch, toolLogSearch)
		self.toolbar7.AddSeparator()
		toolDeleteLogs = self.toolbar7.AddTool(704, _('Delete all logs'), wx.Bitmap(self.currentdir+"/data/logremove.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolDeleteLogs, toolDeleteLogs)

		logMaxSizeLabel = wx.StaticText(self.log, label=_('Notify if the system log file is larger than: '))

		self.logMaxSize = wx.SpinCtrl(self.log, min=1, max=1000)
		logMaxSize = self.conf.get('GENERAL', 'logMaxSize')
		if not logMaxSize: 
			logMaxSize2 = 100
			self.conf.set('GENERAL', 'logMaxSize', str(logMaxSize2))
		else:
			try: logMaxSize2 = int(logMaxSize)
			except: 
				logMaxSize2 = 100
				self.conf.set('GENERAL', 'logMaxSize', str(logMaxSize2))
		self.logMaxSize.SetValue(logMaxSize2)

		logMaxSizeLabel2 = wx.StaticText(self.log, label='MB')

		saveLogMaxSize = wx.Button(self.log, label=_('Save'))
		saveLogMaxSize.Bind(wx.EVT_BUTTON, self.onSaveLogMaxSize)

		h1 = wx.BoxSizer(wx.HORIZONTAL)
		h1.AddSpacer(5)
		h1.Add(logMaxSizeLabel, 0, wx.UP| wx.EXPAND, 10)
		h1.Add(self.logMaxSize, 0, wx.ALL | wx.EXPAND, 5)
		h1.AddSpacer(5)
		h1.Add(logMaxSizeLabel2, 0, wx.UP | wx.EXPAND, 10)
		h1.AddSpacer(5)
		h1.Add(saveLogMaxSize, 0, wx.ALL | wx.EXPAND, 5)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.toolbar7, 0, wx.EXPAND, 0)
		sizer.Add(h1, 0, wx.ALL | wx.EXPAND, 10)
		self.log.SetSizer(sizer)

		if self.conf.get('GENERAL', 'debug') == 'yes': self.toolbar7.ToggleTool(701,True)

	def OnToolDebug(self,e):
		if self.toolbar7.GetToolState(701):
			self.conf.set('GENERAL', 'debug', 'yes')
			self.ShowStatusBarGREEN(_('Debugging mode enabled. Additional info about errors in OpenPlotter apps will be saved in the system log'))
		else:
			self.conf.set('GENERAL', 'debug', 'no')
			self.ShowStatusBarGREEN(_('Debugging mode disabled'))

	def OnToolSeeAll(self,e):
		self.ShowStatusBarYELLOW(_('Reading log, please wait...'))
		self.logger.Clear()
		self.notebook.ChangeSelection(4)
		try:
			path = '/var/log/syslog'
			data = open(path,'r')
			syslog = data.read()
			self.logger.WriteText(syslog)
			self.ShowStatusBarGREEN(_('Done'))
			data.close()
		except Exception as e: 
			self.logger.WriteText('Error reading /var/log/syslog: '+str(e))
			self.ShowStatusBarRED(_('Error reading  log'))
		self.logger.ShowPosition(self.logger.GetLastPosition())

	def OnToolSeeCat(self,e):
		self.ShowStatusBarYELLOW(_('Reading log, please wait...'))
		self.logger.Clear()
		self.notebook.ChangeSelection(4)
		categories = []
		try:
			path = '/var/log/syslog'
			data = open(path,'r')
			while True:
				line = data.readline()
				if not line: break
				items = line.split(' ')
				if not items[5] in categories: categories.append(items[5])
			data.close()
			categories.sort()
			selected = ''
			out = ''
			dlg = selectCategory(categories)
			res = dlg.ShowModal()
			if res == wx.ID_OK: selected = dlg.categories.GetValue()
			dlg.Destroy()
			if selected:
				data = open(path,'r')
				while True:
					line = data.readline()
					if not line: break
					items = line.split(' ')
					if items[5] == selected: out += line
				data.close()
			self.logger.WriteText(out)
			self.ShowStatusBarGREEN(_('Done'))
		except Exception as e: 
			self.logger.WriteText('Error reading /var/log/syslog: '+str(e))
			self.ShowStatusBarRED(_('Error reading log'))
		self.logger.ShowPosition(self.logger.GetLastPosition())

	def OnToolLogSearch(self,e):
		try:
			search = ''
			out = ''
			dlg = logSearch()
			res = dlg.ShowModal()
			if res == wx.ID_OK: search = dlg.search.GetValue()
			dlg.Destroy()
			if search:
				self.ShowStatusBarYELLOW(_('Reading log, please wait...'))
				self.logger.Clear()
				self.notebook.ChangeSelection(4)
				path = '/var/log/syslog'
				data = open(path,'r')
				while True:
					line = data.readline()
					if not line: break
					if search in line: out += line
				data.close()
				self.logger.WriteText(out)
				self.ShowStatusBarGREEN(_('Done'))
		except Exception as e: 
			self.logger.WriteText('Error reading /var/log/syslog: '+str(e))
			self.ShowStatusBarRED(_('Error reading log'))
		self.logger.ShowPosition(self.logger.GetLastPosition())

	def OnToolDeleteLogs(self,e):
		try:
			msg = _('Current and archived system log files will be deleted. A new system log file will be created after reboot.\n\n Are you sure?')
			dlg = wx.MessageDialog(None, msg, _('Question'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
			if dlg.ShowModal() == wx.ID_YES: 
				os.system(self.platform.admin+' rm -f /var/log/syslog*')
				self.ShowStatusBarGREEN(_('Current and archived system log files have been deleted'))
			dlg.Destroy()
		except Exception as e: self.ShowStatusBarRED('Error deleting log files: '+str(e))

	def onSaveLogMaxSize(self,e):
		logMaxSize = self.logMaxSize.GetValue()
		if not logMaxSize: 
			logMaxSize2 = 100
			self.conf.set('GENERAL', 'logMaxSize', str(logMaxSize2))
		else:
			try: 
				logMaxSize2 = int(logMaxSize)
				self.conf.set('GENERAL', 'logMaxSize', str(logMaxSize2))
				self.ShowStatusBarGREEN(_('Done'))
			except: 
				logMaxSize2 = 100
				self.conf.set('GENERAL', 'logMaxSize', str(logMaxSize2))

	###################################################################################

	def pageRpi(self):
		self.toolbar5 = wx.ToolBar(self.raspSettings, style=wx.TB_TEXT)
		toolGpio = self.toolbar5.AddTool(503, _('GPIO Map'), wx.Bitmap(self.currentdir+"/data/chip.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolGpio, toolGpio)
		self.toolbar5.AddSeparator()

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.toolbar5, 0, wx.EXPAND, 0)
		self.raspSettings.SetSizer(sizer)

		if self.platform.isRPI: self.toolbar5.ToggleTool(503,True)
		else: self.toolbar5.EnableTool(503,False)

	def OnToolGpio(self,e):
		dlg = GpioMap()
		res = dlg.ShowModal()
		dlg.Destroy()

	def OnToolStartup(self, e):
		autostartFolder = self.home+'/.config/autostart'
		if not os.path.exists(autostartFolder):
			print('creating autostart directory', autostartFolder)
			os.mkdir(autostartFolder)
		self.autostartFile = self.home+'/.config/autostart/openplotter-startup.desktop'
		if self.toolbar1.GetToolState(102):
			os.system('cp -f '+self.currentdir+'/data/openplotter-startup.desktop '+autostartFolder)
			self.ShowStatusBarGREEN(_('Autostart enabled'))
		else: 
			os.system('rm -f '+self.autostartFile)
			self.ShowStatusBarRED(_('Autostart disabled. Most features will not work!'))

	def OnToolCheck(self, e):
		subprocess.call(['openplotter-startup', 'check'])

	###################################################################################

	def pageApps(self):
		self.listApps = wx.ListCtrl(self.apps, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES, size=(-1,200))
		self.listApps.InsertColumn(0, _('Name'), width=240)
		self.listApps.InsertColumn(1, _('Installed'), width=120)
		self.listApps.InsertColumn(2, _('Candidate'), width=120)
		self.listApps.InsertColumn(3, _('Pending tasks'), width=190)
		self.listApps.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onListAppsSelected)
		self.listApps.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onListAppsDeselected)
		self.listApps.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
		self.listApps.SetTextColour(wx.BLACK)

		self.toolbar6 = wx.ToolBar(self.apps, style=wx.TB_TEXT | wx.TB_HORIZONTAL)
		toolSources = self.toolbar6.AddTool(605, _('Add Sources'), wx.Bitmap(self.currentdir+"/data/sources.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolSources, toolSources)
		toolUpdate = self.toolbar6.AddTool(604, _('Get Candidates'), wx.Bitmap(self.currentdir+"/data/update.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolUpdate, toolUpdate)
		self.refreshButton = self.toolbar6.AddTool(606, _('Refresh'), wx.Bitmap(self.currentdir+"/data/refresh.png"))
		self.Bind(wx.EVT_TOOL, self.OnRefreshButton, self.refreshButton)

		self.toolbar2 = wx.ToolBar(self.apps, style=wx.TB_TEXT | wx.TB_VERTICAL)
		self.installButton = self.toolbar2.AddTool(201, _('Install'), wx.Bitmap(self.currentdir+"/data/install.png"))
		self.Bind(wx.EVT_TOOL, self.OnInstallButton, self.installButton)
		self.uninstallButton = self.toolbar2.AddTool(202, _('Uninstall'), wx.Bitmap(self.currentdir+"/data/uninstall.png"))
		self.Bind(wx.EVT_TOOL, self.OnUninstallButton, self.uninstallButton)
		self.toolbar2.AddSeparator()
		self.openButton = self.toolbar2.AddTool(203, _('Open'), wx.Bitmap(self.currentdir+"/data/open.png"))
		self.Bind(wx.EVT_TOOL, self.OnOpenButton, self.openButton)
		self.logButton = self.toolbar2.AddTool(204, _('Change Log'), wx.Bitmap(self.currentdir+"/data/changelog.png"))
		self.Bind(wx.EVT_TOOL, self.OnLogButton, self.logButton)

		sizerh = wx.BoxSizer(wx.HORIZONTAL)
		sizerh.Add(self.listApps, 1, wx.EXPAND, 0)
		sizerh.Add(self.toolbar2, 0, wx.EXPAND, 0)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.toolbar6, 0, wx.EXPAND, 0)
		sizer.Add(sizerh, 1, wx.EXPAND, 0)

		self.apps.SetSizer(sizer)

		sources = subprocess.check_output(['apt-cache', 'policy']).decode(sys.stdin.encoding)
		for i in self.appsDict:
			item = self.listApps.InsertItem(0, i['name'])
			if i['platform'] == 'rpi': self.listApps.SetItemImage(item, 2)
			else: self.listApps.SetItemImage(item, 1)
			candidate = ''
			missing = False
			for ii in i['sources']:
				if not ii in sources:  missing = ii
			if missing: 
				candidate = _('missing source: ')+missing
			if i['dev'] == 'yes': 
				candidate = _('coming soon')
			if self.platform.isRPI:
				if i['platform'] == 'debian': 
					candidate = _('app only for non Raspberry machines')
			else:
				if i['platform'] == 'rpi': 
					candidate = _('app only for Raspberry machines')
			if candidate:
				self.listApps.SetItem(item, 2, candidate)
			else:
				self.listApps.SetItem(item, 1, _('Press Refresh'))
			self.listApps.SetItemBackgroundColour(item,(200,200,200))

	def OnToolUpdate(self, event=0):
		self.logger.Clear()
		self.notebook.ChangeSelection(4)
		command = self.platform.admin+' apt update'
		popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
		for line in popen.stdout:
			if not 'Warning' in line and not 'WARNING' in line:
				self.logger.WriteText(line)
				self.ShowStatusBarYELLOW(_('Updating packages data, please wait... ')+line)
				self.logger.ShowPosition(self.logger.GetLastPosition())
		self.OnRefreshButton()

	def OnToolSources(self, e):
		self.ShowStatusBarYELLOW(_('Adding packages sources, please wait... '))
		self.logger.Clear()
		self.notebook.ChangeSelection(4)
		command = self.platform.admin+' settingsSourcesInstall'
		popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
		for line in popen.stdout:
			if not 'Warning' in line and not 'WARNING' in line:
				self.logger.WriteText(line)
				self.ShowStatusBarYELLOW(_('Adding packages sources, please wait... ')+line)
				self.logger.ShowPosition(self.logger.GetLastPosition())
		self.ShowStatusBarGREEN(_('Sources updated. Get candidates to see changes'))

	def OnInstallButton(self,e):
		index = self.listApps.GetFirstSelected()
		if index == -1: return
		apps = list(reversed(self.appsDict))
		package = apps[index]['package']
		msg = _('Are you sure you want to install ')+package+_(' and its dependencies?')
		dlg = wx.MessageDialog(None, msg, _('Question'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
		if dlg.ShowModal() == wx.ID_YES:
			self.logger.Clear()
			self.notebook.ChangeSelection(4)
			command = self.platform.admin+' apt install -y '+package
			popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
			for line in popen.stdout:
				if not 'Warning' in line and not 'WARNING' in line:
					self.logger.WriteText(line)
					self.ShowStatusBarYELLOW(_('Installing package, please wait... ')+line)
					self.logger.ShowPosition(self.logger.GetLastPosition())
			postInstall = apps[index]['postInstall']
			if postInstall:
				popen = subprocess.Popen(postInstall, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
				for line in popen.stdout:
					if not 'Warning' in line and not 'WARNING' in line:
						self.logger.WriteText(line)
						self.ShowStatusBarYELLOW(_('Running post-installation scripts, please wait... ')+line)
						self.logger.ShowPosition(self.logger.GetLastPosition())
			if package == 'openplotter-settings':
				wx.MessageBox(_('This app will close to apply the changes.'), _('Info'), wx.OK | wx.ICON_INFORMATION)
				self.Close()
				return
			if apps[index]['reboot'] == 'yes': self.ShowStatusBarRED(_('Done. Restart to apply changes'))
			else: self.ShowStatusBarGREEN(_('Done. Press Refresh'))
		dlg.Destroy()

	def OnUninstallButton(self,e):
		index = self.listApps.GetFirstSelected()
		if index == -1: return
		apps = list(reversed(self.appsDict))
		package = apps[index]['uninstall']
		if self.installedFlag and package == 'openplotter-settings':
			wx.MessageBox(_('You have to uninstall the rest of the apps before uninstalling openplotter-settings.'), _('Info'), wx.OK | wx.ICON_INFORMATION)
			return
		msg = _('Are you sure you want to uninstall ')+package+_(' and its dependencies?')
		dlg = wx.MessageDialog(None, msg, _('Question'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
		if dlg.ShowModal() == wx.ID_YES:
			self.logger.Clear()
			self.notebook.ChangeSelection(4)
			preUninstall = apps[index]['preUninstall']
			if preUninstall:
				popen = subprocess.Popen(preUninstall, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
				for line in popen.stdout:
					if not 'Warning' in line and not 'WARNING' in line:
						self.logger.WriteText(line)
						self.ShowStatusBarYELLOW(_('Running pre-uninstall scripts, please wait... ')+line)
						self.logger.ShowPosition(self.logger.GetLastPosition())	
			command = self.platform.admin+' apt autoremove -y '+package
			popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
			for line in popen.stdout:
				if not 'Warning' in line and not 'WARNING' in line:
					self.logger.WriteText(line)
					self.ShowStatusBarYELLOW(_('Uninstalling packages, please wait... ')+line)
					self.logger.ShowPosition(self.logger.GetLastPosition())
			if apps[index]['reboot'] == 'yes': self.ShowStatusBarRED(_('Done. Restart to apply changes'))
			else: self.ShowStatusBarGREEN(_('Done. Press Refresh'))
		dlg.Destroy()

	def OnRefreshButton(self,e=0):
		appsList = AppsList()
		self.appsDict = appsList.appsDict
		self.readApps()

	def OnOpenButton(self,e):
		index = self.listApps.GetFirstSelected()
		if index == -1: return
		apps = list(reversed(self.appsDict))
		entryPoint = apps[index]['entryPoint']
		popen = subprocess.Popen(entryPoint, shell=True)

	def OnLogButton(self,e):
		index = self.listApps.GetFirstSelected()
		if index == -1: return
		apps = list(reversed(self.appsDict))
		self.logger.Clear()
		self.notebook.ChangeSelection(4)
		command = 'apt changelog '+apps[index]['package']
		popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
		for line in popen.stdout:
			if not 'Warning' in line and not 'WARNING' in line:
				self.logger.WriteText(line)
				self.ShowStatusBarYELLOW(_('Reading changelog, please wait... ')+line)
		self.ShowStatusBarGREEN(_('Done'))

	def readApps(self):
		self.notebook.ChangeSelection(0)
		self.listApps.DeleteAllItems()
		self.ShowStatusBarYELLOW(_('Checking apps list, please wait... '))
		self.installedFlag = False
		sources = subprocess.check_output(['apt-cache', 'policy']).decode(sys.stdin.encoding)
		for i in self.appsDict:
			item = self.listApps.InsertItem(0, i['name'])
			if i['platform'] == 'rpi': self.listApps.SetItemImage(item, 2)
			else: self.listApps.SetItemImage(item, 1)
			
			installed = ''
			candidate = ''
			pending = ''
			command = 'LC_ALL=C apt-cache policy '+i['package']
			popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
			for line in popen.stdout:
				if 'Installed:' in line: installed = line
				if 'Candidate:' in line: candidate = line
			if installed:
				installedL = installed.split(':')
				installed = installedL[1]
			if candidate:
				candidateL = candidate.split(':')
				candidate = candidateL[1]
			if '(none)' in installed: installed = ''

			missing = False
			for ii in i['sources']:
				if not ii in sources:  missing = ii
			if missing: 
				candidate = _('missing source: ')+missing
				self.listApps.SetItemBackgroundColour(item,(200,200,200))

			if i['dev'] == 'yes': 
				candidate = _('coming soon')
				self.listApps.SetItemBackgroundColour(item,(200,200,200))

			if self.platform.isRPI:
				if i['platform'] == 'debian': 
					self.listApps.SetItemBackgroundColour(item,(200,200,200))
					candidate = _('app only for non Raspberry machines')
			else:
				if i['platform'] == 'rpi': 
					self.listApps.SetItemBackgroundColour(item,(200,200,200))
					candidate = _('app only for Raspberry machines')
			
			if not candidate:
				self.listApps.SetItemBackgroundColour(item,(200,200,200))

			if installed and candidate and not missing:
				if installed != candidate: 
					self.listApps.SetItemBackgroundColour(item,(220,255,220))
					pending = _('Install')
				else:
					if 'conf' in i and i['conf']:
						installedL = installed.split('-')
						if self.conf.get('APPS', i['conf']).strip() != installedL[0].strip():
							self.listApps.SetItemBackgroundColour(item,(255,220,220))
							pending = _('Open to apply and refresh')

			self.listApps.SetItem(item, 1, installed)
			self.listApps.SetItem(item, 2, candidate)
			self.listApps.SetItem(item, 3, pending)
			if installed and i['package'] != 'openplotter-settings': self.installedFlag = True

		if not self.platform.isInstalled('openplotter-doc'): self.toolbar1.EnableTool(101,False)
		else:self.toolbar1.EnableTool(101,True)
		self.ShowStatusBarGREEN(_('Done'))

		self.toolbar2.EnableTool(201,False)
		self.toolbar2.EnableTool(202,False)
		self.toolbar2.EnableTool(203,False)
		self.toolbar2.EnableTool(204,False)

	def onListAppsSelected(self, e):
		i = e.GetIndex()
		valid = e and i >= 0
		if not valid: return
		self.onListAppsDeselected()
		if self.listApps.GetItemBackgroundColour(i) != (200,200,200):
			self.toolbar2.EnableTool(201,True)
			self.toolbar2.EnableTool(202,True)
			if self.listApps.GetItemText(i, 1) != '':
				if i != 0:
					self.toolbar2.EnableTool(203,True)
				self.toolbar2.EnableTool(204,True)

	def onListAppsDeselected(self, event=0):
		self.toolbar2.EnableTool(201,False)
		self.toolbar2.EnableTool(202,False)
		self.toolbar2.EnableTool(203,False)
		self.toolbar2.EnableTool(204,False)

	###################################################################################

	def pageOutput(self):
		self.logger = rt.RichTextCtrl(self.output, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_DONTWRAP|wx.LC_SORT_ASCENDING)
		self.logger.SetMargins((10,10))

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.logger, 1, wx.EXPAND, 0)
		self.output.SetSizer(sizer)

###################################################################################

class selectCategory(wx.Dialog):

	def __init__(self,categories):

		wx.Dialog.__init__(self, None, title=_('Select system log category'), size=(500, 150))
		self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		panel = wx.Panel(self)

		self.categories = wx.ComboBox(panel, choices = categories, style=wx.CB_READONLY)

		cancelBtn = wx.Button(panel, wx.ID_CANCEL)
		okBtn = wx.Button(panel, wx.ID_OK)

		actionbox = wx.BoxSizer(wx.HORIZONTAL)
		actionbox.AddStretchSpacer(1)
		actionbox.Add(cancelBtn, 0, wx.LEFT | wx.EXPAND, 10)
		actionbox.Add(okBtn, 0, wx.LEFT | wx.EXPAND, 10)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.AddSpacer(10)
		vbox.Add(self.categories, 0, wx.ALL| wx.EXPAND, 10)
		vbox.AddStretchSpacer(1)
		vbox.Add(actionbox, 0, wx.ALL | wx.EXPAND, 10)

		panel.SetSizer(vbox)
		self.panel = panel

		self.Centre() 

class logSearch(wx.Dialog):

	def __init__(self):

		wx.Dialog.__init__(self, None, title=_('Search in system log file'), size=(500, 150))
		self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		panel = wx.Panel(self)

		self.search = wx.TextCtrl(panel)

		cancelBtn = wx.Button(panel, wx.ID_CANCEL)
		okBtn = wx.Button(panel, wx.ID_OK)

		actionbox = wx.BoxSizer(wx.HORIZONTAL)
		actionbox.AddStretchSpacer(1)
		actionbox.Add(cancelBtn, 0, wx.LEFT | wx.EXPAND, 10)
		actionbox.Add(okBtn, 0, wx.LEFT | wx.EXPAND, 10)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.AddSpacer(10)
		vbox.Add(self.search, 0, wx.ALL| wx.EXPAND, 10)
		vbox.AddStretchSpacer(1)
		vbox.Add(actionbox, 0, wx.ALL | wx.EXPAND, 10)

		panel.SetSizer(vbox)
		self.panel = panel

		self.Centre() 

###################################################################################

def main():
	app = wx.App()
	MyFrame().Show()
	time.sleep(1)
	app.MainLoop()

if __name__ == '__main__':
	main()

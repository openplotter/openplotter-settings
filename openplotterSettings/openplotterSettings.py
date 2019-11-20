#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2019 by Sailoog <https://github.com/openplotter/openplotter-settings>
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

import wx, os, webbrowser, subprocess, sys
import wx.richtext as rt

from .conf import Conf
from .language import Language
from .platform import Platform

class MyFrame(wx.Frame):
	def __init__(self):
		self.conf = Conf()
		self.home = self.conf.home
		self.platform = Platform()
		self.currentdir = os.path.dirname(__file__)
		currentLanguage = self.conf.get('GENERAL', 'lang')
		self.language = Language(self.currentdir,'openplotter-settings',currentLanguage)

		self.appsDict = []

		app = {
		'name': _('OpenPlotter MCS'),
		'platform': 'rpi',
		'package': 'openplotter-mcs',
		'preUninstall': self.platform.admin+' MCSPreUninstall',
		'uninstall': 'openplotter-mcs',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-MCS',
		'postInstall': self.platform.admin+' MCSPostInstall',
		}
		self.appsDict.append(app)

		app = {
		'name': _('OpenPlotter Apps Template'),
		'platform': 'both',
		'package': 'openplotter-myapp',
		'preUninstall': self.platform.admin+' myappPreUninstall',
		'uninstall': 'openplotter-myapp',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-myapp',
		'postInstall': self.platform.admin+' myappPostInstall',
		}
		self.appsDict.append(app)

		app = {
		'name': _('SDR AIS'),
		'platform': 'both',
		'package': 'openplotter-sdr-ais',
		'preUninstall': '',
		'uninstall': 'openplotter-sdr-ais',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'yes',
		'entryPoint': 'openplotter-sdr-ais',
		'postInstall': '',
		}
		self.appsDict.append(app)

		app = {
		'name': _('Kplex'),
		'platform': 'both',
		'package': 'openplotter-kplex',
		'preUninstall': '',
		'uninstall': 'openplotter-kplex',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'yes',
		'entryPoint': 'openplotter-kplex',
		'postInstall': '',
		}
		self.appsDict.append(app)

		app = {
		'name': _('Actions'),
		'platform': 'both',
		'package': 'openplotter-actions',
		'preUninstall': '',
		'uninstall': 'openplotter-actions',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'yes',
		'entryPoint': 'openplotter-actions',
		'postInstall': '',
		}
		self.appsDict.append(app)

		app = {
		'name': _('1W Sensors'),
		'platform': 'rpi',
		'package': 'openplotter-1w',
		'preUninstall': '',
		'uninstall': 'openplotter-1w',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'yes',
		'entryPoint': 'openplotter-1w',
		'postInstall': '',
		}
		self.appsDict.append(app)

		app = {
		'name': _('Signal K Filter'),
		'platform': 'both',
		'package': 'openplotter-SKfilter',
		'preUninstall': '',
		'uninstall': 'openplotter-SKfilter',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-SKfilter',
		'postInstall': '',
		}
		self.appsDict.append(app)

		app = {
		'name': _('Serial Devices Management'),
		'platform': 'both',
		'package': 'openplotter-serial',
		'preUninstall': '',
		'uninstall': 'openplotter-serial',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-serial',
		'postInstall': '',
		}
		self.appsDict.append(app)

		app = {
		'name': _('Moitessier HAT'),
		'platform': 'rpi',
		'package': 'openplotter-moitessier',
		'preUninstall': self.platform.admin+' moitessierPreUninstall',
		'uninstall': 'openplotter-moitessier',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-moitessier',
		'postInstall': self.platform.admin+' moitessierPostInstall',
		}
		self.appsDict.append(app)

		app = {
		'name': _('Pypilot'),
		'platform': 'rpi',
		'package': 'openplotter-pypilot',
		'preUninstall': self.platform.admin+' pypilotPreUninstall',
		'uninstall': 'openplotter-pypilot',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-pypilot',
		'postInstall': self.platform.admin+' pypilotPostInstall',
		}
		self.appsDict.append(app)

		app = {
		'name': _('I2C Sensors'),
		'platform': 'rpi',
		'package': 'openplotter-i2c',
		'preUninstall': self.platform.admin+' i2cPreUninstall',
		'uninstall': 'openplotter-i2c',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-i2c',
		'postInstall': self.platform.admin+' i2cPostInstall',
		}
		self.appsDict.append(app)

		app = {
		'name': _('Network'),
		'platform': 'rpi',
		'package': 'openplotter-network',
		'preUninstall': self.platform.admin+' networkPreUninstall',
		'uninstall': 'openplotter-network',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-network',
		'postInstall': self.platform.admin+' networkPostInstall',
		}
		self.appsDict.append(app)

		app = {
		'name': _('CAN Bus'),
		'platform': 'both',
		'package': 'openplotter-can',
		'preUninstall': self.platform.admin+' canPreUninstall',
		'uninstall': 'openplotter-can',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-can',
		'postInstall': self.platform.admin+' canPostInstall',
		}
		self.appsDict.append(app)
		
		app = {
		'name': _('Dashboards'),
		'platform': 'both',
		'package': 'openplotter-dashboards',
		'preUninstall': '',
		'uninstall': 'openplotter-dashboards',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu','https://repos.influxdata.com/debian','https://packages.grafana.com/oss/deb'],
		'dev': 'no',
		'entryPoint': 'openplotter-dashboards',
		'postInstall': '',
		}
		self.appsDict.append(app)

		app = {
		'name': _('Signal K Installer'),
		'platform': 'both',
		'package': 'openplotter-signalk-installer',
		'preUninstall': self.platform.admin+' signalkPreUninstall',
		'uninstall': 'openplotter-signalk-installer',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu','https://deb.nodesource.com/node_10.x'],
		'dev': 'no',
		'entryPoint': 'openplotter-signalk-installer',
		'postInstall': self.platform.admin+' signalkPostInstall',
		}
		self.appsDict.append(app)

		app = {
		'name': _('XyGrib'),
		'platform': 'rpi',
		'package': 'xygrib',
		'preUninstall': '',
		'uninstall': 'xygrib',
		'sources': ['https://www.free-x.de/debian'],
		'dev': 'no',
		'entryPoint': 'XyGrib',
		'postInstall': self.platform.admin+' python3 '+self.currentdir+'/xygribPostInstall.py',
		}
		self.appsDict.append(app)
		
		app = {
		'name': _('OpenCPN Installer'),
		'platform': 'both',
		'package': 'openplotter-opencpn-installer',
		'preUninstall': '',
		'uninstall': 'openplotter-opencpn-installer opencpn',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu','http://ppa.launchpad.net/opencpn/opencpn/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-opencpn-installer',
		'postInstall': '',
		}
		self.appsDict.append(app)

		app = {
		'name': _('Documentation'),
		'platform': 'both',
		'package': 'openplotter-doc',
		'preUninstall': '',
		'uninstall': 'openplotter-doc',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'x-www-browser /usr/share/openplotter-doc/index.html',
		'postInstall': '',
		}
		self.appsDict.append(app)

		app = {
		'name': _('Settings'),
		'platform': 'both',
		'package': 'openplotter-settings',
		'preUninstall': self.platform.admin+' settingsPreUninstall',
		'uninstall': 'openplotter-settings',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-settings',
		'postInstall': '',
		}
		self.appsDict.append(app)

		wx.Frame.__init__(self, None, title=_('OpenPlotter Settings'), size=(800,444))
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
		toolCheck = self.toolbar1.AddTool(103, _('Check System'), wx.Bitmap(self.currentdir+"/data/check.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolCheck, toolCheck)
		self.toolbar1.AddSeparator()
		toolSources = self.toolbar1.AddTool(105, _('Add Sources'), wx.Bitmap(self.currentdir+"/data/sources.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolSources, toolSources)
		toolUpdate = self.toolbar1.AddTool(104, _('Update Candidates'), wx.Bitmap(self.currentdir+"/data/update.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolUpdate, toolUpdate)
		self.refreshButton = self.toolbar1.AddTool(106, _('Refresh'), wx.Bitmap(self.currentdir+"/data/refresh.png"))
		self.Bind(wx.EVT_TOOL, self.OnRefreshButton, self.refreshButton)
		
		self.notebook = wx.Notebook(self)
		self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onTabChange)
		self.apps = wx.Panel(self.notebook)
		self.genSettings = wx.Panel(self.notebook)
		self.raspSettings = wx.Panel(self.notebook)
		self.output = wx.Panel(self.notebook)
		self.notebook.AddPage(self.apps, _('OpenPlotter Apps'))
		self.notebook.AddPage(self.genSettings, _('General Settings'))
		self.notebook.AddPage(self.raspSettings, _('Raspberry Settings'))
		self.notebook.AddPage(self.output, '')

		self.il = wx.ImageList(24, 24)
		img0 = self.il.Add(wx.Bitmap(self.currentdir+"/data/openplotter-24.png", wx.BITMAP_TYPE_PNG))
		img1 = self.il.Add(wx.Bitmap(self.currentdir+"/data/debian.png", wx.BITMAP_TYPE_PNG))
		img2 = self.il.Add(wx.Bitmap(self.currentdir+"/data/rpi.png", wx.BITMAP_TYPE_PNG))
		img3 = self.il.Add(wx.Bitmap(self.currentdir+"/data/output.png", wx.BITMAP_TYPE_PNG))
		self.notebook.AssignImageList(self.il)
		self.notebook.SetPageImage(0, img0)
		self.notebook.SetPageImage(1, img1)
		self.notebook.SetPageImage(2, img2)
		self.notebook.SetPageImage(3, img3)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.toolbar1, 0, wx.EXPAND)
		vbox.Add(self.notebook, 1, wx.EXPAND)
		self.SetSizer(vbox)

		self.pageGeneral()
		self.pageRpi()
		self.pageOutput()
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

	def OnToolUpdate(self, event=0):
		self.logger.Clear()
		self.notebook.ChangeSelection(3)
		command = self.platform.admin+' apt update'
		popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
		for line in popen.stdout:
			if not 'Warning' in line and not 'WARNING' in line:
				self.logger.WriteText(line)
				self.ShowStatusBarYELLOW(_('Updating packages data, please wait... ')+line)
				self.logger.ShowPosition(self.logger.GetLastPosition())
		self.readApps()

	def OnToolSources(self, e):
		self.ShowStatusBarYELLOW(_('Adding packages sources, please wait... '))
		self.logger.Clear()
		self.notebook.ChangeSelection(3)
		command = self.platform.admin+' settingsSourcesInstall'
		popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
		for line in popen.stdout:
			if not 'Warning' in line and not 'WARNING' in line:
				self.logger.WriteText(line)
				self.ShowStatusBarYELLOW(_('Adding packages sources, please wait... ')+line)
				self.logger.ShowPosition(self.logger.GetLastPosition())
		self.ShowStatusBarGREEN(_('Added sources. Update candidates to see changes'))

	def OnToolLanguage(self, event): 
		short = 'en'
		name = self.languageList.GetValue()
		for i in self.language.available:
			if name == i[0]: short = i[1]
		self.conf.set('GENERAL', 'lang', short)
		wx.MessageBox(_('Close and open again the window to see changes.'), _('Info'), wx.OK | wx.ICON_INFORMATION)

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
		starupLabel = wx.StaticText(self.genSettings, label=_('Startup'))
		self.toolbar4 = wx.ToolBar(self.genSettings, style=wx.TB_TEXT)
		toolDelay = self.toolbar4.AddCheckTool(401, _('Delay (seconds)'), wx.Bitmap(self.currentdir+"/data/delay.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolDelay, toolDelay)
		self.delay = wx.TextCtrl(self.toolbar4, 402)
		tooldelay = self.toolbar4.AddControl(self.delay)
		self.toolbar4.AddSeparator()
		toolPlay = self.toolbar4.AddCheckTool(403, _('Play'), wx.Bitmap(self.currentdir+"/data/play.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolPlay, toolPlay)
		self.pathFile = wx.TextCtrl(self.toolbar4, 404, size=(415,-1))
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
			else: self.toolbar4.ToggleTool(401,False)
		else:
			self.conf.set('GENERAL', 'delay', '')
			self.ShowStatusBarGREEN(_('Removed delay at startup'))

	def OnToolMaxi(self,e):
		if self.toolbar3.GetToolState(303):
			self.conf.set('GENERAL', 'maximize', '1')
			self.ShowStatusBarGREEN(_('OpenPlotter apps will open maximized'))
		else:
			self.conf.set('GENERAL', 'maximize', '0')
			self.ShowStatusBarGREEN(_('Disabled maximized OpenPlotter apps'))

	def pageRpi(self):
		self.toolbar5 = wx.ToolBar(self.raspSettings, style=wx.TB_TEXT)
		toolScreensaver = self.toolbar5.AddCheckTool(501, _('Disable Screensaver'), wx.Bitmap(self.currentdir+"/data/screen.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolScreensaver, toolScreensaver)
		self.toolbar5.AddSeparator()
		toolHeadless = self.toolbar5.AddCheckTool(502, _('Headless'), wx.Bitmap(self.currentdir+"/data/headless.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolHeadless, toolHeadless)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.toolbar5, 0, wx.EXPAND, 0)
		self.raspSettings.SetSizer(sizer)

		if self.platform.isRPI:
			screensaver = self.conf.get('GENERAL', 'screensaver')
			if screensaver == '1': 
				self.toolbar5.ToggleTool(501,True)
			config = open('/boot/config.txt', 'r')
			data = config.read()
			config.close()
			if not '#hdmi_force_hotplug=1' in data:
				self.toolbar5.ToggleTool(502,True)
		else: 
			self.toolbar5.EnableTool(501,False)
			self.toolbar5.EnableTool(502,False)

	def OnToolScreensaver(self, e):
		if self.toolbar5.GetToolState(501):
			self.conf.set('GENERAL', 'screensaver', '1')
			subprocess.call(['xset', 's', 'noblank'])
			subprocess.call(['xset', 's', 'off'])
			subprocess.call(['xset', '-dpms'])
		else: 
			self.conf.set('GENERAL', 'screensaver', '0')
			subprocess.call(['xset', 's', 'blank'])
			subprocess.call(['xset', 's', 'on'])
			subprocess.call(['xset', '+dpms'])

	def OnToolHeadless(self, e):
		onoff = self.toolbar5.GetToolState(502)
		file = open('/boot/config.txt', 'r')
		file1 = open(self.home+'/config.txt', 'w')
		exists = False
		while True:
			line = file.readline()
			if not line: break
			if onoff and 'hdmi_force_hotplug=1' in line: 
				file1.write('hdmi_force_hotplug=1\n')
				exists = True
			elif not onoff and 'hdmi_force_hotplug=1' in line: 
				file1.write('#hdmi_force_hotplug=1\n')
				exists = True
			else: file1.write(line)
		if onoff and not exists: 
			file1.write('\nhdmi_force_hotplug=1\n')
		file.close()
		file1.close()

		reset = False
		if os.system('diff '+self.home+'/config.txt /boot/config.txt > /dev/null'):
			os.system(self.platform.admin+' mv '+self.home+'/config.txt /boot')
			reset = True
		else: os.system('rm -f '+self.home+'/config.txt')

		if reset: self.ShowStatusBarGREEN(_('Changes will be applied after restarting'))

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

	def pageApps(self):
		self.listApps = wx.ListCtrl(self.apps, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES, size=(-1,200))
		self.listApps.InsertColumn(0, _('Name'), width=260)
		self.listApps.InsertColumn(1, _('Installed'), width=130)
		self.listApps.InsertColumn(2, _('Candidate'), width=280)
		self.listApps.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onListAppsSelected)
		self.listApps.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onListAppsDeselected)
		self.listApps.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

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

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(self.listApps, 1, wx.EXPAND, 0)
		sizer.Add(self.toolbar2, 0)
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


	def OnInstallButton(self,e):
		index = self.listApps.GetFirstSelected()
		if index == -1: return
		apps = list(reversed(self.appsDict))
		package = apps[index]['package']
		msg = _('Are you sure you want to install ')+package+_(' and its dependencies?')
		dlg = wx.MessageDialog(None, msg, _('Question'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
		if dlg.ShowModal() == wx.ID_YES:
			self.logger.Clear()
			self.notebook.ChangeSelection(3)
			command = self.platform.admin+' apt -y install '+package
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
			self.ShowStatusBarGREEN(_('Done'))
			dlg.Destroy()
			self.readApps()
		else: dlg.Destroy()

	def OnUninstallButton(self,e):
		index = self.listApps.GetFirstSelected()
		if index == -1: return
		apps = list(reversed(self.appsDict))
		package = apps[index]['uninstall']
		if self.installedFlag and package == 'openplotter-settings':
			wx.MessageBox(_('You have to uninstall the rest of apps before uninstalling openplotter-settings.'), _('Info'), wx.OK | wx.ICON_INFORMATION)
			return
		msg = _('Are you sure you want to uninstall ')+package+_(' and its dependencies?')
		dlg = wx.MessageDialog(None, msg, _('Question'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
		if dlg.ShowModal() == wx.ID_YES:
			self.logger.Clear()
			self.notebook.ChangeSelection(3)
			preUninstall = apps[index]['preUninstall']
			if preUninstall:
				popen = subprocess.Popen(preUninstall, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
				for line in popen.stdout:
					if not 'Warning' in line and not 'WARNING' in line:
						self.logger.WriteText(line)
						self.ShowStatusBarYELLOW(_('Running pre-uninstall scripts, please wait... ')+line)
						self.logger.ShowPosition(self.logger.GetLastPosition())	
			command = self.platform.admin+' apt -y autoremove '+package
			popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
			for line in popen.stdout:
				if not 'Warning' in line and not 'WARNING' in line:
					self.logger.WriteText(line)
					self.ShowStatusBarYELLOW(_('Uninstalling packages, please wait... ')+line)
					self.logger.ShowPosition(self.logger.GetLastPosition())
			self.ShowStatusBarGREEN(_('Done'))
			dlg.Destroy()
			self.readApps()
		else: dlg.Destroy()

	def OnRefreshButton(self,e):
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
		self.notebook.ChangeSelection(3)
		command = 'apt changelog '+apps[index]['package']
		popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
		for line in popen.stdout:
			if not 'Warning' in line and not 'WARNING' in line:
				self.logger.WriteText(line)
				self.ShowStatusBarYELLOW(_('Reading changelog, please wait... ')+line)
				self.logger.ShowPosition(self.logger.GetLastPosition())
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

			if installed and candidate:
				if installed != candidate: self.listApps.SetItemBackgroundColour(item,(220,255,220))

			self.listApps.SetItem(item, 1, installed)
			self.listApps.SetItem(item, 2, candidate)
			if installed and i['package'] != 'openplotter-settings': self.installedFlag = True

		if not self.platform.isInstalled('openplotter-doc'): self.toolbar1.EnableTool(101,False)
		else:self.toolbar1.EnableTool(101,True)
		self.ShowStatusBarGREEN(_('Done'))

		self.toolbar2.EnableTool(201,False)
		self.toolbar2.EnableTool(202,False)
		self.toolbar2.EnableTool(203,False)
		self.toolbar2.EnableTool(204,False)
	
	def pageOutput(self):
		self.logger = rt.RichTextCtrl(self.output, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_DONTWRAP|wx.LC_SORT_ASCENDING)
		self.logger.SetMargins((10,10))

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.logger, 1, wx.EXPAND, 0)
		self.output.SetSizer(sizer)

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

def main():
	app = wx.App()
	MyFrame().Show()
	app.MainLoop()

if __name__ == '__main__':
	main()

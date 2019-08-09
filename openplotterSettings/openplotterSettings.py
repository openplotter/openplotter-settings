#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2015 by sailoog <https://github.com/sailoog/openplotter>
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

import wx, os, webbrowser, subprocess
import wx.richtext as rt

from .conf import Conf
from .language import Language
from .platform import Platform

class MyFrame(wx.Frame):
	def __init__(self):
		self.conf = Conf()
		self.home = self.conf.home
		self.platform = Platform()
		self.isRPI = self.platform.isRPI
		self.currentdir = os.path.dirname(__file__)
		currentLanguage = self.conf.get('GENERAL', 'lang')
		self.language = Language(self.currentdir,'openplotter-settings',currentLanguage)

		wx.Frame.__init__(self, None, title=_('OpenPlotter Settings'), size=(800,444))
		self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		icon = wx.Icon(self.currentdir+"/data/openplotter-settings.png", wx.BITMAP_TYPE_PNG)
		self.SetIcon(icon)

		self.toolbar1 = wx.ToolBar(self, style=wx.TB_TEXT)
		toolHelp = self.toolbar1.AddTool(101, _('Help'), wx.Bitmap(self.currentdir+"/data/help.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolHelp, toolHelp)
		self.toolbar1.AddSeparator()
		toolStartup = self.toolbar1.AddCheckTool(102, _('Autostart'), wx.Bitmap(self.currentdir+"/data/autostart.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolStartup, toolStartup)
		if self.conf.get('GENERAL', 'autostart') == '1': self.toolbar1.ToggleTool(102,True)
		toolCheck = self.toolbar1.AddTool(103, _('Check System'), wx.Bitmap(self.currentdir+"/data/check.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolCheck, toolCheck)
		self.toolbar1.AddSeparator()
		toolSources = self.toolbar1.AddTool(105, _('Add sources'), wx.Bitmap(self.currentdir+"/data/sources.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolSources, toolSources)
		toolUpdate = self.toolbar1.AddTool(104, _('Update Data'), wx.Bitmap(self.currentdir+"/data/update.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolUpdate, toolUpdate)
		
		self.notebook = wx.Notebook(self)
		self.apps = wx.Panel(self.notebook)
		self.genSettings = wx.Panel(self.notebook)
		self.raspSettings = wx.Panel(self.notebook)
		self.output = wx.Panel(self.notebook)
		self.notebook.AddPage(self.apps, _('OpenPlotter Apps'))
		self.notebook.AddPage(self.genSettings, _('General Settings'))
		self.notebook.AddPage(self.raspSettings, _('Raspberry Settings'))
		self.notebook.AddPage(self.output, _('Output'))

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

		self.CreateStatusBar()
		font_statusBar = self.GetStatusBar().GetFont()
		font_statusBar.SetWeight(wx.BOLD)
		self.GetStatusBar().SetFont(font_statusBar)
		self.Centre(True) 
		self.Show(True)

		self.pageApps()
		self.onListAppsDeselected()
		self.pageGeneral()
		self.pageRpi()
		self.pageOutput()

	def ShowStatusBar(self, w_msg, colour):
		self.GetStatusBar().SetForegroundColour(colour)
		self.SetStatusText(w_msg)

	def ShowStatusBarRED(self, w_msg):
		self.ShowStatusBar(w_msg, wx.RED)

	def ShowStatusBarGREEN(self, w_msg):
		self.ShowStatusBar(w_msg, wx.GREEN)

	def ShowStatusBarBLACK(self, w_msg):
		self.ShowStatusBar(w_msg, wx.BLACK) 

	def ShowStatusBarYELLOW(self, w_msg):
		self.ShowStatusBar(w_msg,(255,140,0)) 

	def OnToolHelp(self, event): 
		url = "/usr/share/openplotter-doc/settings/settings_app.html"
		webbrowser.open(url, new=2)

	def OnToolTranslate(self, event): 
		url = "https://crowdin.com/project/openplotter"
		webbrowser.open(url, new=2)

	def OnToolUpdate(self, event=0):
		self.logger.Clear()
		self.notebook.ChangeSelection(3)
		command = 'sudo apt update'
		popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
		for line in popen.stdout:
			self.logger.WriteText(line)
			self.ShowStatusBarYELLOW(_('Updating packages data, please wait... ')+line)
			self.logger.ShowPosition(self.logger.GetLastPosition())
		self.ShowStatusBarGREEN(_('Done. Now you can check if there are available updates'))
		self.readApps()

	def OnToolSources(self, e):
		self.ShowStatusBarYELLOW(_('Adding packages sources, please wait... '))
		os.system('sudo cp -f '+self.currentdir+'/data/sources/openplotter.list /etc/apt/sources.list.d')
		os.system('sudo cp -f '+self.currentdir+'/data/sources/preferences /etc/apt/preferences.d')
		os.system('sudo apt-key add - < '+self.currentdir+'/data/sources/opencpn.gpg.key')
		os.system('sudo apt-key add - < '+self.currentdir+'/data/sources/openplotter.gpg.key')
		os.system('sudo apt-key add - < '+self.currentdir+'/data/sources/grafana.gpg.key')
		os.system('sudo apt-key add - < '+self.currentdir+'/data/sources/influxdb.gpg.key')
		os.system('sudo apt-key add - < '+self.currentdir+'/data/sources/nodesource.gpg.key')
		self.OnToolUpdate()

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

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.toolbar3, 0, wx.EXPAND, 0)
		self.genSettings.SetSizer(sizer)

	def pageRpi(self):
		pass
		#TODO disable is not on RPI
		#if self.isRPI:

	def OnToolStartup(self, e):
		autostartFolder = self.home+'/.config/autostart'
		if not os.path.exists(autostartFolder):
			print('creating autostart directory', autostartFolder)
			os.mkdir(autostartFolder)
		self.autostartFile = self.home+'/.config/autostart/openplotter-startup.desktop'
		if self.toolbar1.GetToolState(102):
			os.system('cp -f '+self.currentdir+'/data/openplotter-startup.desktop '+autostartFolder)
			self.conf.set('GENERAL', 'autostart', '1')
			self.ShowStatusBarGREEN(_('Autostart enabled'))
		else: 
			os.system('rm -f '+self.autostartFile)
			self.conf.set('GENERAL', 'autostart', '0')
			self.ShowStatusBarRED(_('Autostart disabled. Most features will not work!'))

	def OnToolCheck(self, e):
		subprocess.call(['openplotter-startup', 'check'])

	def pageApps(self):
		self.listApps = wx.ListCtrl(self.apps, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES, size=(-1,200))
		self.listApps.InsertColumn(0, _('Name'), width=260)
		self.listApps.InsertColumn(1, _('Installed'), width=130)
		self.listApps.InsertColumn(2, _('Candidate'), width=290)
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
		self.changelogButton = self.toolbar2.AddTool(204, _('Changelog'), wx.Bitmap(self.currentdir+"/data/text.png"))
		self.Bind(wx.EVT_TOOL, self.OnChangelogButtonButton, self.changelogButton)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(self.listApps, 1, wx.EXPAND, 0)
		sizer.Add(self.toolbar2, 0)
		self.apps.SetSizer(sizer)

		self.readApps()

	def OnInstallButton(self,e):
		index = self.listApps.GetFirstSelected()
		if index == -1: return
		apps = list(reversed(self.apps))
		package = apps[index]['package']
		msg = _('Are you sure you want to install ')+package+_(' and its dependencies?')
		dlg = wx.MessageDialog(None, msg, _('Question'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
		if dlg.ShowModal() == wx.ID_YES:
			self.logger.Clear()
			self.notebook.ChangeSelection(3)
			command = 'sudo apt -y install '+package
			popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
			for line in popen.stdout:
				self.logger.WriteText(line)
				self.ShowStatusBarYELLOW(_('Installing package, please wait... ')+line)
				self.logger.ShowPosition(self.logger.GetLastPosition())
			postInstallation = apps[index]['postInstallation']
			if postInstallation:
				popen = subprocess.Popen(postInstallation, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
				for line in popen.stdout:
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
		apps = list(reversed(self.apps))
		package = apps[index]['uninstall']
		if self.installedFlag and package == 'openplotter-settings':
			wx.MessageBox(_('You have to uninstall the rest of apps before uninstalling openplotter-settings.'), _('Info'), wx.OK | wx.ICON_INFORMATION)
			return
		msg = _('Are you sure you want to uninstall ')+package+_(' and its dependencies?')
		dlg = wx.MessageDialog(None, msg, _('Question'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
		if dlg.ShowModal() == wx.ID_YES:
			self.logger.Clear()
			self.notebook.ChangeSelection(3)
			command = 'sudo apt -y autoremove '+package
			popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
			for line in popen.stdout:
				self.logger.WriteText(line)
				self.ShowStatusBarYELLOW(_('Uninstalling packages, please wait... ')+line)
				self.logger.ShowPosition(self.logger.GetLastPosition())
			self.ShowStatusBarGREEN(_('Done'))
			dlg.Destroy()
			self.readApps()
		else: dlg.Destroy()

	def OnChangelogButtonButton(self,e):
		index = self.listApps.GetFirstSelected()
		if index == -1: return
		apps = list(reversed(self.apps))
		self.logger.Clear()
		self.notebook.ChangeSelection(3)
		command = 'apt changelog '+apps[index]['package']
		popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
		for line in popen.stdout:
			self.logger.WriteText(line)
			self.ShowStatusBarYELLOW(_('Reading changelog, please wait... ')+line)
		self.ShowStatusBarGREEN(_('Done'))

	def OnOpenButton(self,e):
		index = self.listApps.GetFirstSelected()
		if index == -1: return
		apps = list(reversed(self.apps))
		entryPoint = apps[index]['entryPoint']
		popen = subprocess.Popen(entryPoint, shell=True)

	def readApps(self):
		self.listApps.DeleteAllItems()
		self.apps = []

		app = {
		'name': _('Fake app only for desktops'),
		'platform': 'debian',
		'package': 'openplotter-fake',
		'uninstall': 'openplotter-fake',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-fake',
		'postInstallation': '',
		}
		self.apps.append(app)

		app = {
		'name': _('Signal K Filters'),
		'platform': 'both',
		'package': 'openplotter-signalk-filters',
		'uninstall': 'openplotter-signalk-filters',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'yes',
		'entryPoint': 'openplotter-signalk-filters',
		'postInstallation': '',
		}
		self.apps.append(app)

		app = {
		'name': _('SDR AIS'),
		'platform': 'both',
		'package': 'openplotter-sdr-ais',
		'uninstall': 'openplotter-sdr-ais',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'yes',
		'entryPoint': 'openplotter-sdr-ais',
		'postInstallation': '',
		}
		self.apps.append(app)

		app = {
		'name': _('Kplex'),
		'platform': 'both',
		'package': 'openplotter-kplex',
		'uninstall': 'openplotter-kplex',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'yes',
		'entryPoint': 'openplotter-kplex',
		'postInstallation': '',
		}
		self.apps.append(app)

		app = {
		'name': _('Dashboards'),
		'platform': 'both',
		'package': 'openplotter-dashboards',
		'uninstall': 'openplotter-dashboards',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'yes',
		'entryPoint': 'openplotter-dashboards',
		'postInstallation': '',
		}
		self.apps.append(app)

		app = {
		'name': _('Actions'),
		'platform': 'both',
		'package': 'openplotter-actions',
		'uninstall': 'openplotter-actions',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'yes',
		'entryPoint': 'openplotter-actions',
		'postInstallation': '',
		}
		self.apps.append(app)

		app = {
		'name': _('CAN Devices Management'),
		'platform': 'both',
		'package': 'openplotter-can',
		'uninstall': 'openplotter-can',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'yes',
		'entryPoint': 'openplotter-can',
		'postInstallation': '',
		}
		self.apps.append(app)

		app = {
		'name': _('Moitessier HAT'),
		'platform': 'rpi',
		'package': 'openplotter-moitessier',
		'uninstall': 'openplotter-moitessier',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'yes',
		'entryPoint': 'openplotter-moitessier',
		'postInstallation': '',
		}
		self.apps.append(app)

		app = {
		'name': _('Pypilot'),
		'platform': 'rpi',
		'package': 'openplotter-pypilot',
		'uninstall': 'openplotter-pypilot',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'yes',
		'entryPoint': 'openplotter-pypilot',
		'postInstallation': '',
		}
		self.apps.append(app)

		app = {
		'name': _('1W Sensors'),
		'platform': 'rpi',
		'package': 'openplotter-1w',
		'uninstall': 'openplotter-1w',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'yes',
		'entryPoint': 'openplotter-1w',
		'postInstallation': '',
		}
		self.apps.append(app)

		app = {
		'name': _('I2C Sensors'),
		'platform': 'rpi',
		'package': 'openplotter-i2c',
		'uninstall': 'openplotter-i2c',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'yes',
		'entryPoint': 'openplotter-i2c',
		'postInstallation': '',
		}
		self.apps.append(app)

		app = {
		'name': _('Serial Devices Management'),
		'platform': 'both',
		'package': 'openplotter-serial',
		'uninstall': 'openplotter-serial',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'yes',
		'entryPoint': 'openplotter-serial',
		'postInstallation': '',
		}
		self.apps.append(app)

		app = {
		'name': _('Network'),
		'platform': 'rpi',
		'package': 'openplotter-network',
		'uninstall': 'openplotter-network',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-network',
		'postInstallation': 'sudo networkPostInstallation',
		}
		self.apps.append(app)

		app = {
		'name': _('Signal K Installer'),
		'platform': 'both',
		'package': 'openplotter-signalk-installer',
		'uninstall': 'openplotter-signalk-installer',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu','https://deb.nodesource.com/node_10.x'],
		'dev': 'no',
		'entryPoint': 'openplotter-signalk-installer',
		'postInstallation': 'sudo signalkPostInstallation',
		}
		self.apps.append(app)

		app = {
		'name': _('OpenCPN Installer'),
		'platform': 'both',
		'package': 'openplotter-opencpn-installer',
		'uninstall': 'openplotter-opencpn-installer opencpn',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu','http://ppa.launchpad.net/opencpn/opencpn/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-opencpn-installer',
		'postInstallation': '',
		}
		self.apps.append(app)

		app = {
		'name': _('Documentation'),
		'platform': 'both',
		'package': 'openplotter-doc',
		'uninstall': 'openplotter-doc',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'x-www-browser /usr/share/openplotter-doc/index.html',
		'postInstallation': '',
		}
		self.apps.append(app)

		app = {
		'name': _('Settings'),
		'platform': 'both',
		'package': 'openplotter-settings',
		'uninstall': 'openplotter-settings',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-settings',
		'postInstallation': '',
		}
		self.apps.append(app)

		self.installedFlag = False
		sources = subprocess.check_output(['apt-cache', 'policy']).decode()
		for i in self.apps:
			item = self.listApps.InsertItem(0, i['name'])
			if i['platform'] == 'rpi': self.listApps.SetItemImage(item, 2)
			else: self.listApps.SetItemImage(item, 1)

			installed = ''
			candidate = ''
			command = 'LANG=C apt-cache policy '+i['package']
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

			if self.isRPI:
				if i['platform'] == 'debian': 
					self.listApps.SetItemBackgroundColour(item,(200,200,200))
					candidate = _('app only for non Raspberry machines')
			else:
				if i['platform'] == 'rpi': 
					self.listApps.SetItemBackgroundColour(item,(200,200,200))
					candidate = _('app only for Raspberry machines')
			
			if not candidate:
				self.listApps.SetItemBackgroundColour(item,(200,200,200))

			self.listApps.SetItem(item, 1, installed)
			self.listApps.SetItem(item, 2, candidate)
			if installed and i['package'] != 'openplotter-settings': self.installedFlag = True

		if not self.platform.isInstalled('openplotter-doc'): self.toolbar1.EnableTool(101,False)
		else:self.toolbar1.EnableTool(101,True)
	
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

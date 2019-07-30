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

from .conf import Conf
from .language import Language
from .platform import Platform

class MyFrame(wx.Frame):
	def __init__(self):
		self.conf = Conf()
		self.home = self.conf.home
		platform = Platform()
		self.isRPI = platform.isRPI
		self.currentdir = os.path.dirname(__file__)
		currentLanguage = self.conf.get('GENERAL', 'lang')
		self.language = Language('openplotter-settings',currentLanguage)

		wx.Frame.__init__(self, None, title='OpenPlotter Settings', size=(800,444))
		self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		icon = wx.Icon(self.currentdir+"/data/48x48.png", wx.BITMAP_TYPE_PNG)
		self.SetIcon(icon)

		self.toolbar1 = wx.ToolBar(self, style=wx.TB_TEXT)
		toolHelp = self.toolbar1.AddTool(101, 'Help', wx.Bitmap(self.currentdir+"/data/help.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolHelp, toolHelp)
		self.toolbar1.AddSeparator()
		langList = []
		for i in self.language.available:
			langList.append(i[0])
		self.languageList = wx.ComboBox(self.toolbar1, 102, _('Language'), choices=langList, size=(150,-1), style=wx.CB_DROPDOWN)
		toolLanguage = self.toolbar1.AddControl(self.languageList)
		self.Bind(wx.EVT_COMBOBOX, self.OnToolLanguage, toolLanguage)
		toolTranslate = self.toolbar1.AddTool(103, 'Translate', wx.Bitmap(self.currentdir+"/data/crowdin.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolTranslate, toolTranslate)
		self.toolbar1.AddSeparator()
		toolUpdate = self.toolbar1.AddTool(104, 'Update Package Data', wx.Bitmap(self.currentdir+"/data/package.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolUpdate, toolUpdate)
		
		self.notebook = wx.Notebook(self)
		self.apps = wx.Panel(self.notebook)
		self.genSettings = wx.Panel(self.notebook)
		self.notebook.AddPage(self.apps, _('OpenPlotter Apps'))
		self.notebook.AddPage(self.genSettings, 'General Settings')
		self.il = wx.ImageList(24, 24)
		img0 = self.il.Add(wx.Bitmap(self.currentdir+"/data/24x24.png", wx.BITMAP_TYPE_PNG))
		img1 = self.il.Add(wx.Bitmap(self.currentdir+"/data/debian.png", wx.BITMAP_TYPE_PNG))
		img2 = self.il.Add(wx.Bitmap(self.currentdir+"/data/rpi.png", wx.BITMAP_TYPE_PNG))
		self.notebook.AssignImageList(self.il)
		self.notebook.SetPageImage(0, img0)
		self.notebook.SetPageImage(1, img1)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.toolbar1, 0, wx.EXPAND)
		vbox.Add(self.notebook, 1, wx.EXPAND)
		self.SetSizer(vbox)

		if self.isRPI:
			self.raspSettings = wx.Panel(self.notebook)
			self.notebook.AddPage(self.raspSettings, 'Raspberry Settings')
			self.notebook.SetPageImage(2, img2)

		self.CreateStatusBar()
		self.Centre(True) 
		self.Show(True)

		self.pageApps()
		self.onListAppsDeselected()

	def OnToolHelp(self, event): 
		url = "/usr/share/openplotter-doc/settings/settings_app.html"
		webbrowser.open(url, new=2)

	def OnToolHelp2(self, event): 
		url = "/usr/share/openplotter-doc/settings/settings_app.html"
		webbrowser.open(url, new=2)

	def OnToolTranslate(self, event): 
		url = "https://crowdin.com/project/openplotter"
		webbrowser.open(url, new=2)

	def OnToolUpdate(self, event): 
		command = 'sudo apt update'
		popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
		for line in popen.stdout:
			self.SetStatusText(_('Updating, please wait: ')+line)
		self.readApps()
		self.SetStatusText(_('Updated: ')+line)


	def OnToolLanguage(self, event): 
		short = 'en'
		name = self.languageList.GetValue()
		for i in self.language.available:
			if name == i[0]: short = i[1]
		self.conf.set('GENERAL', 'lang', short)
		wx.MessageBox(_('Close and open again the window to see changes.'), _('Info'), wx.OK | wx.ICON_INFORMATION)

	def pageApps(self):
		self.listApps = wx.ListCtrl(self.apps, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL, size=(-1,200))
		self.listApps.InsertColumn(0, _('Name'), width=250)
		self.listApps.InsertColumn(1, _('Installed Version'), width=200)
		self.listApps.InsertColumn(2, _('Candidate Version'), width=200)
		self.listApps.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onListAppsSelected)
		self.listApps.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onListAppsDeselected)
		self.listApps.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

		self.toolbar2 = wx.ToolBar(self.apps, style=wx.TB_TEXT | wx.TB_VERTICAL)
		toolHelp2 = self.toolbar2.AddTool(201, 'Help', wx.Bitmap(self.currentdir+"/data/help.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolHelp2, toolHelp2)
		self.toolbar2.AddSeparator()

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(self.listApps, 1, wx.EXPAND, 0)
		sizer.Add(self.toolbar2, 0)
		self.apps.SetSizer(sizer)

		self.readApps()

	def readApps(self):
		self.listApps.DeleteAllItems()
		apps = []

		app = {
		'name': _('Fake app'),
		'platform': 'debian',
		'package': 'openplotter-fake',
		}
		apps.append(app)

		app = {
		'name': _('Network'),
		'platform': 'rpi',
		'package': 'openplotter-network',
		}
		apps.append(app)

		app = {
		'name': _('Documentation'),
		'platform': 'both',
		'package': 'openplotter-doc',
		}
		apps.append(app)

		app = {
		'name': _('Settings'),
		'platform': 'both',
		'package': 'openplotter-settings',
		}
		apps.append(app)

		for i in apps:
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

			#last = self.listApps.GetItemCount()-1
			if not candidate: 
				candidate = _('Coming soon')
				self.listApps.SetItemBackgroundColour(item,(200,200,200))

			if self.isRPI:
				if i['platform'] == 'debian': 
					self.listApps.SetItemBackgroundColour(item,(200,200,200))
					candidate = _('App only for non Raspberry machines')
			else:
				if i['platform'] == 'rpi': 
					self.listApps.SetItemBackgroundColour(item,(200,200,200))
					candidate = _('App only for Raspberry machines')

			self.listApps.SetItem(item, 1, installed)
			self.listApps.SetItem(item, 2, candidate)

	def onListAppsSelected(self, e):
		i = e.GetIndex()
		valid = e and i >= 0
		if not valid: return
		st = self.listApps.GetItemBackgroundColour(i) != (200,200,200)
		self.toolbar2.EnableTool(201,st)

	def onListAppsDeselected(self, event=0):
		self.toolbar2.EnableTool(201,False)

def main():
	app = wx.App()
	MyFrame().Show()
	app.MainLoop()

if __name__ == '__main__':
	main()

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

import wx, os, webbrowser

from .conf import Conf
from .language import Language

class MyFrame(wx.Frame):
	def __init__(self):
		self.conf = Conf()
		self.home = self.conf.home
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
		langList = []
		for i in self.language.available:
			langList.append(i[0])
		self.languageList = wx.ComboBox(self.toolbar1, 102, _('Language'), choices=langList, size=(150,-1), style=wx.CB_DROPDOWN)
		toolLanguage = self.toolbar1.AddControl(self.languageList)
		self.Bind(wx.EVT_COMBOBOX, self.OnToolLanguage, toolLanguage)
		self.toolbar1.AddSeparator()
		
		self.notebook = wx.Notebook(self)
		self.apps = wx.Panel(self.notebook)
		self.genSettings = wx.Panel(self.notebook)
		self.notebook.AddPage(self.apps, _('OpenPlotter Apps'))
		self.notebook.AddPage(self.genSettings, 'General Settings')
		il = wx.ImageList(24, 24)
		img0 = il.Add(wx.Bitmap(self.currentdir+"/data/24x24.png", wx.BITMAP_TYPE_PNG))
		img1 = il.Add(wx.Bitmap(self.currentdir+"/data/debian.png", wx.BITMAP_TYPE_PNG))
		self.notebook.AssignImageList(il)
		self.notebook.SetPageImage(0, img0)
		self.notebook.SetPageImage(1, img1)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.toolbar1, 0, wx.EXPAND)
		vbox.Add(self.notebook, 1, wx.EXPAND)
		self.SetSizer(vbox)

		rpi = False
		try:
			modelfile = open('/sys/firmware/devicetree/base/model', 'r', 2000)
			rpimodel = modelfile.read()
			modelfile.close()
			if 'Raspberry' in rpimodel: rpi = True
		except: pass
		if rpi:
			self.raspSettings = wx.Panel(self.notebook)
			self.notebook.AddPage(self.raspSettings, 'Raspberry Settings')
			img2 = il.Add(wx.Bitmap(self.currentdir+"/data/rpi.png", wx.BITMAP_TYPE_PNG))
			self.notebook.SetPageImage(2, img2)

		self.CreateStatusBar()
		self.Centre(True) 
		self.Show(True)

		self.pageApps()

	def OnToolHelp(self, event): 
		url = "/usr/share/openplotter-doc/index.html"
		webbrowser.open(url, new=2)

	def OnToolLanguage(self, event): 
		short = 'en'
		name = self.languageList.GetValue()
		for i in self.language.available:
			if name == i[0]: short = i[1]
		self.conf.set('GENERAL', 'lang', short)
		wx.MessageBox(_('Close and open again the window to see changes.'), _('Info'), wx.OK | wx.ICON_INFORMATION)

	def pageApps(self):
		self.listApps = wx.ListCtrl(self.apps, -1, style=wx.LC_REPORT | wx.BORDER_SIMPLE | wx.LC_SINGLE_SEL, size=(-1,200))
		self.listApps.InsertColumn(0, '', width=30)
		self.listApps.InsertColumn(1, _('Name'), width=100)
		self.listApps.InsertColumn(2, _('System'), width=60)
		self.listApps.InsertColumn(3, _('Version'), width=60)
		self.listApps.InsertColumn(4, _('Update'), width=200)
		self.listApps.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onListAppsSelected)
		self.listApps.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onListAppsDeselected)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.listApps, 1, wx.EXPAND, 0)
		self.apps.SetSizer(sizer)

	def onListAppsSelected(self, event):
		pass

	def onListAppsDeselected(self, event):
		pass

def main():
	app = wx.App()
	MyFrame().Show()
	app.MainLoop()

if __name__ == '__main__':
	main()

#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2019 by sailoog <https://github.com/sailoog/openplotter>
#                     e-sailing <https://github.com/e-sailing/openplotter>
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
import wx, os, sys, time, threading, subprocess
import wx.richtext as rt
from .conf import Conf
from .language import Language

class MyFrame(wx.Frame):
	def __init__(self, mode):
		self.conf = Conf()
		self.mode = mode
		currentLanguage = self.conf.get('GENERAL', 'lang')
		self.currentdir = os.path.dirname(__file__)
		self.language = Language(self.currentdir,'openplotter-settings',currentLanguage)

		self.ttimer = 100
		self.logger_data=False
		self.warnings_flag=False
		self.autoclose = 0

		wx.Frame.__init__(self, None, title=_('Starting OpenPlotter'), style=wx.STAY_ON_TOP, size=(800,475))
		self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		icon = wx.Icon(self.currentdir+"/data/openplotter-48.png", wx.BITMAP_TYPE_PNG)
		self.SetIcon(icon)
		self.CreateStatusBar()
		font_statusBar = self.GetStatusBar().GetFont()
		font_statusBar.SetWeight(wx.BOLD)
		self.GetStatusBar().SetFont(font_statusBar)
		if self.mode == 'start': self.SetStatusText(_('Starting OpenPlotter. Please wait for all services to start'))
		else: self.SetStatusText(_('Checking OpenPlotter system. Please wait for all services to be checked'))
		self.Centre()

		panel = wx.Panel(self, wx.ID_ANY)

		self.logger = rt.RichTextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_DONTWRAP|wx.LC_SORT_ASCENDING)
		self.logger.SetMargins((10,10))

		self.closeButton =wx.Button(panel, label=_('Close'))
		self.closeButton.Bind(wx.EVT_BUTTON, self.OnCloseButton)
		self.closeButton.Disable()

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.logger, 1, wx.ALL | wx.EXPAND, 5)
		vbox.Add(self.closeButton, 0, wx.ALL | wx.EXPAND, 5)
		panel.SetSizer(vbox)

		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.refresh, self.timer)

		self.thread1=threading.Thread(target=self.starting)
		if not self.thread1.isAlive(): self.thread1.start()

		self.timer.Start(self.ttimer)

	def refresh(self,event):
		if self.logger_data:
			if isinstance(self.logger_data, str):
				self.logger.BeginTextColour((55, 55, 55))
				self.logger.WriteText(self.logger_data)
			if isinstance(self.logger_data, dict):
				if self.logger_data['green']:
					self.logger.WriteText(' | ')
					self.logger.BeginTextColour((0, 255, 0))
					self.logger.WriteText(self.logger_data['green'])
					self.logger.EndTextColour()
				if self.logger_data['black']:
					self.logger.WriteText(' | ')
					self.logger.BeginTextColour((55, 55, 55))
					self.logger.WriteText(self.logger_data['black'])
					self.logger.EndTextColour()
				if self.logger_data['red']:
					self.warnings_flag = True
					self.logger.Newline()
					self.logger.BeginTextColour((255, 0, 0))
					self.logger.WriteText(self.logger_data['red'])
					self.logger.EndTextColour()
				self.logger.Newline()
			self.logger_data = False
		if self.autoclose > 0:
			rest = round(self.autoclose - time.time())
			if self.autoclose < time.time():
				self.OnCloseButton()
		if not self.thread1.isAlive():
			if not self.warnings_flag:
				if self.mode == 'start': self.OnCloseButton()
				else:
					self.closeButton.Enable()
					self.GetStatusBar().SetForegroundColour(wx.BLACK)
					self.SetStatusText(_('There are no warnings. Closing in ')+str(rest)+_(' seconds'))
			else:
				self.closeButton.Enable()
				self.GetStatusBar().SetForegroundColour(wx.RED)
				self.SetStatusText(_('There are some warnings. Check your system. Closing in ')+str(rest)+_(' seconds'))

	def add_logger_data(self, msg):
		while self.logger_data:
			time.sleep(0.1)
		self.logger_data=msg

	def starting(self):

		self.add_logger_data(_('Checking OpenPlotter autostart...'))
		if self.conf.get('GENERAL', 'autostart') != '1':
			self.add_logger_data({'green':'','black':'','red':_('Autostart is not enabled and most features will not work. Please select "Autostart" in "OpenPlotter Settings"')})
		else:
			self.add_logger_data({'green':_('enabled'),'black':'','red':''})

		startup = False
		try:
			from openplotterOpencpnInstaller import startup
		except:pass
		if startup: self.processApp(startup)

		startup = False
		try:
			from openplotterNetwork import startup
		except:pass
		if startup: self.processApp(startup)

		self.autoclose=time.time() + 60

	def processApp(self, startup):
		if self.mode == 'start':
			start = startup.Start(self.conf)
			initialMessage = start.initialMessage
			if initialMessage: 
				self.add_logger_data(initialMessage)
				result = start.start()
				if result: self.add_logger_data(result)
		check = startup.Check(self.conf)
		initialMessage = check.initialMessage
		if initialMessage: 
			self.add_logger_data(initialMessage)
			result = check.check()
			if result: self.add_logger_data(result)

	def OnCloseButton(self,e=0):
		self.timer.Stop()
		self.Destroy()


def print_help():
	print('This is part of OpenPlotter software')
	print('It starts or checks all needed server/services/background processes')
	print('Options are:')
	print('   openplotter-startup start   (does only run on X display desktop)')
	print('   openplotter-startup check   (does only run on X display desktop)')
	print('this:')
	print('   openplotter-startup -h')

def main():
	if len(sys.argv)>1:
		if sys.argv[1]=='start':
			app = wx.App()
			MyFrame('start').Show()
			app.MainLoop()
		elif sys.argv[1]=='check':
			app = wx.App()
			MyFrame('check').Show()
			app.MainLoop()
		else: print_help()
	else: print_help()

if __name__ == '__main__':
	main()

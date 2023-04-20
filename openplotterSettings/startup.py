#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2022 by sailoog <https://github.com/openplotter/openplotter-settings>
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

import wx, os, sys, time, threading, subprocess, importlib, configparser
import wx.richtext as rt
from .conf import Conf
from .language import Language
from .platform import Platform
from .ports import Ports
from .serialPorts import SerialPorts
from .gpio import Gpio
from .appsList import AppsList

class MyFrame(wx.Frame):
	def __init__(self, mode):
		self.conf = Conf()
		self.mode = mode
		self.platform = Platform()
		self.isRPI = self.platform.isRPI
		self.currentLanguage = self.conf.get('GENERAL', 'lang')
		self.currentdir = os.path.dirname(os.path.abspath(__file__))
		self.language = Language(self.currentdir,'openplotter-settings',self.currentLanguage)
		self.debug = self.conf.get('GENERAL', 'debug')

		self.ttimer = 100
		self.logger_data=False
		self.warnings_flag=False

		if self.mode == 'start': title = _('Starting OpenPlotter')
		else: title = _('Checking OpenPlotter')

		wx.Frame.__init__(self, None, title=title, style = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP, size=(800,444))
		self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		icon = wx.Icon(self.currentdir+"/data/openplotter-48.png", wx.BITMAP_TYPE_PNG)
		self.SetIcon(icon)
		self.CreateStatusBar()
		font_statusBar = self.GetStatusBar().GetFont()
		font_statusBar.SetWeight(wx.BOLD)
		self.GetStatusBar().SetFont(font_statusBar)
		if self.mode == 'start': self.SetStatusText(_('Please DO NOT CLOSE THIS WINDOW until all services have been started'))
		else: self.SetStatusText(_('Please wait for all services to be checked'))

		panel = wx.Panel(self, wx.ID_ANY)

		self.logger = rt.RichTextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_DONTWRAP|wx.LC_SORT_ASCENDING)
		self.logger.SetMargins((10,10))

		self.toolbar1 = wx.ToolBar(panel, style=wx.TB_TEXT | wx.TB_VERTICAL)
		toolClose = self.toolbar1.AddTool(102, _('Close'), wx.Bitmap(self.currentdir+"/data/close.png"))
		self.Bind(wx.EVT_TOOL, self.OnCloseButton, toolClose)
		self.toolbar1.EnableTool(102,False)
		self.toolbar1.AddSeparator()
		toolRescue = self.toolbar1.AddCheckTool(101, _('Rescue'), wx.Bitmap(self.currentdir+"/data/rescue.png"))
		self.Bind(wx.EVT_TOOL, self.onToolRescue, toolRescue)
		if self.conf.get('GENERAL', 'rescue') == 'yes': self.toolbar1.ToggleTool(101,True)
		
		vbox = wx.BoxSizer(wx.HORIZONTAL)
		vbox.Add(self.logger, 1, wx.ALL | wx.EXPAND, 5)
		vbox.Add(self.toolbar1, 0, wx.ALL | wx.EXPAND, 0)
		panel.SetSizer(vbox)

		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.refresh, self.timer)

		self.thread1=threading.Thread(target=self.starting)
		self.thread1.daemon = True
		if not self.thread1.is_alive(): self.thread1.start()

		self.timer.Start(self.ttimer)

		maxi = self.conf.get('GENERAL', 'maximize')
		if maxi == '1': self.Maximize()
		
		self.Centre() 

	def refresh(self,event):
		if self.logger_data:
			if isinstance(self.logger_data, int):
				self.toolbar1.EnableTool(102,True)
				if self.warnings_flag:
					self.GetStatusBar().SetForegroundColour(wx.RED)
					self.SetStatusText(_('There are some warnings. Check your system. Closing in ')+str(self.logger_data)+_(' seconds'))
				else:
					if self.mode == 'start': self.OnCloseButton()
					else:
						self.GetStatusBar().SetForegroundColour(wx.BLACK)
						self.SetStatusText(_('There are no warnings. Closing in ')+str(self.logger_data)+_(' seconds'))
			elif isinstance(self.logger_data, str):
				self.logger.BeginTextColour((55, 55, 55))
				self.logger.WriteText(self.logger_data)
				self.logger.ShowPosition(self.logger.GetLastPosition())
			elif isinstance(self.logger_data, dict):
				if self.logger_data['green']:
					self.logger.WriteText(' | ')
					self.logger.BeginTextColour((0, 130, 0))
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
					self.logger.BeginTextColour((130, 0, 0))
					self.logger.WriteText(' ↳'+self.logger_data['red'])
					self.logger.EndTextColour()
				self.logger.Newline()
				self.logger.ShowPosition(self.logger.GetLastPosition())
			self.logger_data = False

		if not self.thread1.is_alive(): self.OnCloseButton()

	def add_logger_data(self, msg):
		while self.logger_data:
			time.sleep(0.1)
		self.logger_data=msg

	def startApp(self, startup):
		start = startup.Start(self.conf,self.currentLanguage)
		initialMessage = start.initialMessage
		if initialMessage: 
			self.add_logger_data(initialMessage)
			result = start.start()
			if result: self.add_logger_data(result)

	def checkApp(self, startup):
		check = startup.Check(self.conf,self.currentLanguage)
		initialMessage = check.initialMessage
		if initialMessage: 
			self.add_logger_data(initialMessage)
			result = check.check()
			if result: self.add_logger_data(result)

	def starting(self):
		delay = self.conf.get('GENERAL', 'delay')
		if self.mode == 'start':
			try:
				if delay:
					self.add_logger_data(_('Applying delay of ')+delay+_(' seconds...'))
					time.sleep(int(delay))
					self.add_logger_data({'green':'','black':_('done'),'red':''})
			except:self.add_logger_data({'green':'','black':'','red':_('Delay failed. Is it a number?')})
		else:
			try:
				if delay:
					self.add_logger_data(_('A startup delay will apply'))
					checkDelay = int(delay)
					self.add_logger_data({'green':'','black':delay+_(' seconds'),'red':''})
			except:self.add_logger_data({'green':'','black':'','red':_('Delay failed. Is it a number?')})

		appsList = AppsList()
		appsDict = appsList.appsDict
		if self.mode == 'start':
			for i in appsDict:
				name = i['module']
				if name:
					startup = False
					try:
						startup = importlib.import_module(name+'.startup')
						if startup: self.startApp(startup)
					except Exception as e: 
						if self.debug == 'yes': print(str(e))

		self.add_logger_data(_('Checking touchscreen optimization...'))
		touchscreen = self.conf.get('GENERAL', 'touchscreen')
		gtk_overlay_scrolling = False
		conf_file = self.conf.home+'/.config/gtk-3.0/settings.ini'
		if os.path.exists(conf_file):
			data_conf = configparser.ConfigParser()
			data_conf.read(conf_file)
			gtk_overlay_scrolling = data_conf.get('Settings','gtk-overlay-scrolling') 
		css = False
		css_file = self.conf.home+'/.config/gtk-3.0/gtk.css'
		if os.path.exists(css_file):
			with open(css_file) as f:
				if '/*openplotter settings*/' in f.read(): css = True
		if touchscreen == '1':
			if not gtk_overlay_scrolling or gtk_overlay_scrolling == 'true' or not css:
				self.add_logger_data({'green':'','black':'','red':_('There are errors in the configuration files, try to reinitialize this setting.')})
			else:
				self.add_logger_data({'green':'','black':_('enabled'),'red':''})
		else:
			if gtk_overlay_scrolling == 'false' or css:
				self.add_logger_data({'green':'','black':'','red':_('There are errors in the configuration files, try to reinitialize this setting.')})
			else:
				self.add_logger_data({'green':'','black':_('disabled'),'red':''})

		if self.isRPI:
			try: config = open('/boot/config.txt', 'r')
			except: config = open('/boot/firmware/config.txt', 'r')
			data = config.read()
			config.close()
			self.add_logger_data(_('Checking Power off management...'))
			if 'dtoverlay=gpio-poweroff' in data and not '#dtoverlay=gpio-poweroff' in data: self.add_logger_data({'green':'','black':_('enabled'),'red':''})
			else: self.add_logger_data({'green':'','black':_('disabled'),'red':''})
			self.add_logger_data(_('Checking Shutdown management...'))
			if 'dtoverlay=gpio-shutdown' in data and not '#dtoverlay=gpio-shutdown' in data: self.add_logger_data({'green':'','black':_('enabled'),'red':''})
			else: self.add_logger_data({'green':'','black':_('disabled'),'red':''})

		self.add_logger_data(_('Checking OpenPlotter autostart...'))
		if not os.path.exists(self.conf.home+'/.config/autostart/openplotter-startup.desktop'):
			self.add_logger_data({'green':'','black':'','red':_('Autostart is not enabled and most features will not work. Please select "Autostart" in "OpenPlotter Settings"')})
		else:
			self.add_logger_data({'green':'','black':_('enabled'),'red':''})

		self.add_logger_data(_('Checking rescue mode...'))
		rescue = self.conf.get('GENERAL', 'rescue')
		if rescue == 'yes': 
			self.add_logger_data({'green':'','black':'','red':_('enabled')})
		else:
			self.add_logger_data({'green':'','black':_('disabled'),'red':''})

		self.add_logger_data(_('Checking debugging mode...'))
		
		if self.debug == 'yes': 
			self.add_logger_data({'green':'','black':'','red':_('enabled')})
		else:
			self.add_logger_data({'green':'','black':_('disabled'),'red':''})

		logMaxSize = self.conf.get('GENERAL', 'logMaxSize')
		if logMaxSize:
			self.add_logger_data(_('Checking system log file size...'))
			try:
				mb = os.path.getsize("/var/log/syslog")/1e+6
				if mb >= int(logMaxSize): self.add_logger_data({'green':'','black':'','red':_('System log file size: ')+str(round(mb,2))+' MB'})
				else: self.add_logger_data({'green':'','black':_('System log file size: ')+str(round(mb,2))+' MB','red':''})
			except Exception as e: self.add_logger_data({'green':'','black':'','red':str(e)})
		
		self.add_logger_data(_('Checking OpenPlotter packages source...'))
		sources = subprocess.check_output(['apt-cache', 'policy']).decode(sys.stdin.encoding)
		if 'https://dl.cloudsmith.io/public/openplotter/openplotter/deb/debian' in sources:
			self.add_logger_data({'green':'','black':_('added'),'red':''})
		else: self.add_logger_data({'green':'','black':'','red':_('There are missing packages sources. Please add sources in "OpenPlotter Settings".')})

		for i in appsDict:
			name = i['module']
			if name:
				startup = False
				try:
					startup = importlib.import_module(name+'.startup')
					if startup: self.checkApp(startup)
				except Exception as e: 
					if self.debug == 'yes': print(str(e))
					
		try:
			self.add_logger_data(_('Checking serial connections conflicts...'))
			allSerialPorts = SerialPorts()
			conflicts = allSerialPorts.conflicts()
			if conflicts:
				red = _('There are conflicts between the following serial connections:')
				for i in conflicts: 
					red += '\n    '+i
				self.add_logger_data({'green':'','black':'','red':red})
			else: self.add_logger_data({'green':'','black':_('no conflicts'),'red':''})
		except Exception as e: self.add_logger_data({'green':'','black':'','red':str(e)})

		try:
			self.add_logger_data(_('Checking network connections conflicts...'))
			self.ports = Ports()
			conflicts = self.ports.conflicts()
			if conflicts:
				red = _('There are conflicts between the following server connections:')
				for i in conflicts: 
					red += '\n    '+i['description']+' ('+i['mode']+'): '+i['type']+' '+i['address']+':'+i['port']
				self.add_logger_data({'green':'','black':'','red':red})
			else: self.add_logger_data({'green':'','black':_('no conflicts'),'red':''})
		except Exception as e: self.add_logger_data({'green':'','black':'','red':str(e)})

		if self.isRPI:
			try:
				self.add_logger_data(_('Checking GPIO conflicts...'))
				gpios = Gpio()
				gpios.addUsedGpios()
				gpioMap = gpios.gpioMap
				red = ''
				for i in gpioMap:
					if not i['shared'] and len(i['usedBy']) > 1:
						if not red: red = _('There are GPIO conflicts between the following apps:')
						line = ''
						for ii in i['usedBy']:
							if line: line += ', '
							line += ii['app']+' - '+ii['id']
						red += '\n    '+line
				if red: self.add_logger_data({'green':'','black':'','red':red})
				else: self.add_logger_data({'green':'','black':_('no conflicts'),'red':''})
			except Exception as e: self.add_logger_data({'green':'','black':'','red':str(e)})

		try:
			play = self.conf.get('GENERAL', 'play')
			if play: subprocess.Popen(['cvlc', '--play-and-exit', play])
		except Exception as e: self.add_logger_data({'green':'','black':'','red':str(e)})

		if self.mode == 'start': self.add_logger_data(_('STARTUP FINISHED'))
		else: self.add_logger_data(_('CHECK SYSTEM FINISHED'))

		c = 60
		while True:
			time.sleep(1)
			if c < 1: break
			else: self.add_logger_data(c)
			c = c - 1

	def OnCloseButton(self,e=0):
		self.timer.Stop()
		self.Destroy()

	def onToolRescue(self,e=0):
		if self.toolbar1.GetToolState(101): self.conf.set('GENERAL', 'rescue', 'yes')
		else: self.conf.set('GENERAL', 'rescue', 'no')

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
			time.sleep(1)
			app.MainLoop()
		elif sys.argv[1]=='check':
			app = wx.App()
			MyFrame('check').Show()
			time.sleep(1)
			app.MainLoop()
		else: print_help()
	else: print_help()

if __name__ == '__main__':
	main()

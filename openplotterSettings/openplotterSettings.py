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

import wx, os, webbrowser, subprocess, sys, time, configparser
import wx.richtext as rt

from .conf import Conf
from .language import Language
from .platform import Platform
from .version import version
from .appsList import AppsList
from .gpio import GpioMap, Gpio
from .ports import Ports

class MyFrame(wx.Frame):
	def __init__(self):
		self.conf = Conf()
		self.home = self.conf.home
		self.platform = Platform()
		self.currentdir = os.path.dirname(os.path.abspath(__file__))
		if self.conf.get('GENERAL', 'debug') == 'yes': self.debug = True
		else: self.debug = False
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
		self.toolbar1.AddSeparator()
		toolAddresses = self.toolbar1.AddTool(104, _('Network'), wx.Bitmap(self.currentdir+"/data/ports.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolAddresses, toolAddresses)

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


	def OnToolAddresses(self, e):
		allPorts = Ports()
		usedPorts = allPorts.getUsedPorts()
		ip_hostname = subprocess.check_output(['hostname']).decode(sys.stdin.encoding)[:-1]
		ip_info = subprocess.check_output(['hostname', '-I']).decode(sys.stdin.encoding)
		ips = ip_info.split()
		self.logger.Clear()
		self.notebook.ChangeSelection(3)
		self.logger.BeginTextColour((55, 55, 55))
		for i in usedPorts:
			self.logger.BeginBold()
			self.logger.WriteText(i['description']+' ('+i['mode']+')')
			self.logger.EndBold()
			self.logger.Newline()
			if i['address'] == 'localhost' or i['address'] == '127.0.0.1':
				self.logger.WriteText(i['type']+' '+str(ip_hostname)+'.local:'+str(i['port']))
				self.logger.Newline()
				for ip in ips:
					if ip[0:7]=='169.254': pass
					elif ':' in ip: pass
					else: 
						self.logger.WriteText(i['type']+' '+str(ip)+':'+str(i['port']))
						self.logger.Newline()
			else: 
				self.logger.WriteText(i['type']+' '+i['address']+':'+str(i['port']))
				self.logger.Newline()
		self.logger.EndTextColour()
		
		conflicts = allPorts.conflicts()
		if conflicts:
			red = ''
			self.logger.BeginTextColour((130, 0, 0))
			for i in conflicts:
				self.logger.Newline()
				self.logger.WriteText(i['description']+' ('+i['mode']+'): '+i['type']+' '+i['address']+':'+i['port'])
			self.logger.EndTextColour()
			self.ShowStatusBarRED(_('There are conflicts between server connections'))
		else: self.ShowStatusBarGREEN(_('No conflicts between server connections'))
		self.logger.ShowPosition(self.logger.GetLastPosition())

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
		toolTouch = self.toolbar3.AddCheckTool(305, _('Touchscreen'), wx.Bitmap(self.currentdir+"/data/touchscreen.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolTouch, toolTouch)
		toolMaxi = self.toolbar3.AddCheckTool(303, _('Maximize apps'), wx.Bitmap(self.currentdir+"/data/resize.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolMaxi, toolMaxi)

		self.toolbar10 = wx.ToolBar(self.genSettings, style=wx.TB_TEXT)
		keyboardList = []
		try:
			items = os.listdir('/usr/share/matchbox-keyboard')
			for i in items:
				if i[0:8] == 'keyboard' and '.xml' in i: keyboardList.append(i)
		except Exception as e: 
			if self.debug: print('Error getting virtual keyboard layouts: '+str(e))
		self.keyboardsList = wx.ComboBox(self.toolbar10, 1001, _('Keyboard layout'), choices=keyboardList, size=(200,-1), style=wx.CB_DROPDOWN)
		toolKeyboards = self.toolbar10.AddControl(self.keyboardsList)
		self.Bind(wx.EVT_COMBOBOX, self.OnToolKeyboards, toolKeyboards)
		toolMatchbox= self.toolbar10.AddTool(1002, _('Virtual keyboard'), wx.Bitmap(self.currentdir+"/data/keyboard.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolMatchbox, toolMatchbox)
		currentKeyboard = self.conf.get('GENERAL', 'keyboard')
		if currentKeyboard: self.keyboardsList.SetValue(currentKeyboard)
		else:
			try:
				folder = self.home+'/.matchbox'
				if not os.path.exists(folder): os.mkdir(folder)
				os.system('cp -f '+self.currentdir+'/data/keyboards/keyboard-EN.xml '+folder+'/keyboard.xml')
				self.conf.set('GENERAL', 'keyboard', 'keyboard-EN.xml')
				self.keyboardsList.SetValue('keyboard-EN.xml')
			except Exception as e: 
				if self.debug: print('Error setting virtual keyboard layout: '+str(e))
		self.toolbar10.AddSeparator()
		toolDebug = self.toolbar10.AddCheckTool(1003, _('Debugging'), wx.Bitmap(self.currentdir+"/data/bug.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolDebug, toolDebug)

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
		sizer.Add(self.toolbar10, 0, wx.EXPAND, 0)
		sizer.Add(starupLabel, 0, wx.ALL | wx.EXPAND, 10)
		sizer.Add(self.toolbar4, 0, wx.EXPAND, 0)
		self.genSettings.SetSizer(sizer)

		touchscreen = self.conf.get('GENERAL', 'touchscreen')
		if touchscreen == '1': 
			self.toolbar3.ToggleTool(305,True)

		maxi = self.conf.get('GENERAL', 'maximize')
		if maxi == '1': 
			self.toolbar3.ToggleTool(303,True)
			self.Maximize()

		out = subprocess.check_output('echo $XDG_SESSION_TYPE', shell=True).decode(sys.stdin.encoding)
		if 'wayland' in out: self.toolbar10.EnableTool(1001,False)

		if self.conf.get('GENERAL', 'debug') == 'yes': self.toolbar10.ToggleTool(1003,True)

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

	def OnToolDebug(self,e):
		if self.toolbar10.GetToolState(1003):
			self.conf.set('GENERAL', 'debug', 'yes')
			self.ShowStatusBarGREEN(_('Debugging mode enabled. Additional info about errors in OpenPlotter apps will be saved in the system log'))
		else:
			self.conf.set('GENERAL', 'debug', 'no')
			self.ShowStatusBarGREEN(_('Debugging mode disabled'))

	def OnToolFile(self,e):
		dlg = wx.FileDialog(self, message=_('Choose a file'), defaultDir='/usr/share/sounds/openplotter', defaultFile='',
							wildcard=_('Audio files') + ' (*.mp3)|*.mp3|' + _('All files') + ' (*.*)|*.*',
							style=wx.FD_OPEN | wx.FD_CHANGE_DIR)
		if dlg.ShowModal() == wx.ID_OK:
			file_path = dlg.GetPath()
			self.pathFile.SetValue(file_path)
			self.OnToolPlay()
		dlg.Destroy()

	def OnToolMatchbox(self,e=0):
		subprocess.call(['pkill', '-f', 'matchbox-keyboard'])
		out = subprocess.check_output('echo $XDG_SESSION_TYPE', shell=True).decode(sys.stdin.encoding)
		if 'wayland' in out: subprocess.Popen('toggle-wvkbd')
		else: subprocess.Popen('matchbox-keyboard')

	def OnToolKeyboards(self,e=0):
		if self.keyboardsList.GetSelection() == -1: return
		try:
			file = self.keyboardsList.GetValue()
			folder = self.home+'/.matchbox'
			if not os.path.exists(folder): os.mkdir(folder)
			os.system('cp -f /usr/share/matchbox-keyboard/'+file+' '+folder+'/keyboard.xml')
			self.conf.set('GENERAL', 'keyboard', file)
			self.OnToolMatchbox()
		except Exception as e: 
			if self.debug: print('Error setting virtual keyboard layout: '+str(e))

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

	def setTouchSystem(self,path,enabled):
		if os.path.exists(path):
			css = path+'/gtk-3.0/gtk.css'
			if not os.path.exists(path+'/gtk-3.0'): os.mkdir(path+'/gtk-3.0')
			if not os.path.exists(css):
				file = open(path+'/gtk-3.0/gtk.css', 'w')
				file.write('')
				file.close()

			os.system('cp -f '+css+' '+css+'_back')
			file = open(css, 'r')
			exists = False
			out = ''
			while True:
				line = file.readline()
				if not line: break
				if '@import url("openplotter.css");' in line:
					exists = True
					if enabled: out += line
					else: pass
				else: out += line
			if enabled and not exists: out += '@import url("openplotter.css");\n'
			file.close()
			try: 
				file = open(css, 'w')
				file.write(out)
				file.close()
			except Exception as e:
				os.system('cp -f '+css+'_back '+css)
				if self.debug: print('Error setting gtk css: '+str(e))

			try:
				opcss = path+'/gtk-3.0/openplotter.css'
				file = open(opcss, 'w')
				file.write('scrollbar slider { min-width: 20px;min-height: 20px;border-radius: 22px;border: 5px solid transparent; }')
				file.close()
			except Exception as e:
				if self.debug: print('Error setting gtk css: '+str(e))


	def setTouchOpencpn(self,path,enabled):
		if os.path.exists(path):
			data_conf = configparser.ConfigParser()
			data_conf.read(path)
			if enabled: data_conf.set('Settings','MobileTouch','1')
			else: data_conf.set('Settings','MobileTouch','0')
			with open(path, 'w') as file:
				data_conf.write(file)

	def OnToolTouch(self,e):
		subprocess.call(['pkill', '-15', 'opencpn'])
		try: subprocess.call(['flatpak', 'kill', 'org.opencpn.OpenCPN'])
		except: pass
		if self.toolbar3.GetToolState(305):
			self.conf.set('GENERAL', 'touchscreen', '1')
			subprocess.call([self.platform.admin, 'python3', self.currentdir+'/service.py', 'touch', '1'])
			self.setTouchSystem(self.home+'/.var/app/org.opencpn.OpenCPN/config','1')
			self.setTouchOpencpn(self.home+'/.opencpn/opencpn.conf',True)
			self.setTouchOpencpn(self.home+'/.var/app/org.opencpn.OpenCPN/config/opencpn/opencpn.conf',True)
			self.ShowStatusBarGREEN(_('Enabled. Changes will be applied after the next reboot'))
		else:
			self.conf.set('GENERAL', 'touchscreen', '0')
			subprocess.call([self.platform.admin, 'python3', self.currentdir+'/service.py', 'touch', ''])
			self.setTouchSystem(self.home+'/.var/app/org.opencpn.OpenCPN/config','')
			self.setTouchOpencpn(self.home+'/.opencpn/opencpn.conf',False)
			self.setTouchOpencpn(self.home+'/.var/app/org.opencpn.OpenCPN/config/opencpn/opencpn.conf',False)
			self.ShowStatusBarGREEN(_('Disabled. Changes will be applied after the next reboot'))

	def OnToolMaxi(self,e=0):
		if self.toolbar3.GetToolState(303):
			self.conf.set('GENERAL', 'maximize', '1')
			self.ShowStatusBarGREEN(_('OpenPlotter apps will open maximized'))
			self.Maximize(True)
		else:
			self.conf.set('GENERAL', 'maximize', '0')
			self.ShowStatusBarGREEN(_('Disabled maximized OpenPlotter apps'))
			self.Maximize(False)

	###################################################################################

	def pageRpi(self):
		self.toolbar5 = wx.ToolBar(self.raspSettings, style=wx.TB_TEXT)
		toolGpio = self.toolbar5.AddTool(503, _('GPIO Map'), wx.Bitmap(self.currentdir+"/data/chip.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolGpio, toolGpio)
		self.toolbar5.AddSeparator()
		toolbacklightInstall = self.toolbar5.AddCheckTool(504, _('Install backlight'), wx.Bitmap(self.currentdir+"/data/brightness-install.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolbacklightInstall, toolbacklightInstall)
		toolbacklightSet = self.toolbar5.AddTool(505, _('Set backlight'), wx.Bitmap(self.currentdir+"/data/brightness.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolbacklightSet, toolbacklightSet)
		self.toolbar5.AddSeparator()
		toolWayland = self.toolbar5.AddCheckTool(506, 'Wayland', wx.Bitmap(self.currentdir+"/data/wayland.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolWayland, toolWayland)
		self.toolbar5.AddSeparator()
		toolHotspot = self.toolbar5.AddCheckTool(507, _('Hotspot+Client'), wx.Bitmap(self.currentdir+"/data/ap.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolHotspot, toolHotspot)

		powerLabel = wx.StaticText(self.raspSettings, label=_('Shutdown Management'))

		self.toolbar8 = wx.ToolBar(self.raspSettings, style=wx.TB_TEXT)
		toolShutdown = self.toolbar8.AddCheckTool(801, _('Shutdown'), wx.Bitmap(self.currentdir+"/data/shutdown.png"))
		self.Bind(wx.EVT_TOOL, self.onToolShutdown, toolShutdown)
		separatorLabel0 = wx.StaticText(self.toolbar8, 808, label='    ')
		toolSeparatorLabel0= self.toolbar8.AddControl(separatorLabel0)
		self.gpioShutdown = wx.TextCtrl(self.toolbar8, 802, style=wx.CB_READONLY)
		toolGpioShutdown = self.toolbar8.AddControl(self.gpioShutdown)
		toolSetGpioShutdown= self.toolbar8.AddTool(803, _('GPIO'), wx.Bitmap(self.currentdir+"/data/chip.png"))
		self.Bind(wx.EVT_TOOL, self.onToolSetGpioShutdown, toolSetGpioShutdown)
		self.transitionShutdown = wx.ComboBox(self.toolbar8, 804, _('Transition'), choices=[_('low->high'),_('high->low')], size=(150,-1), style=wx.CB_DROPDOWN)
		toolTransitionShutdown = self.toolbar8.AddControl(self.transitionShutdown)
		separatorLabel = wx.StaticText(self.toolbar8, 807, label='    ')
		toolSeparatorLabel= self.toolbar8.AddControl(separatorLabel)
		self.gpioPullShutdown = wx.ComboBox(self.toolbar8, 805, 'GPIO Pull', choices=['pull-up','pull-down',_('off')], size=(150,-1), style=wx.CB_DROPDOWN)
		toolGpioPullShutdown = self.toolbar8.AddControl(self.gpioPullShutdown)
		self.toolbar8.AddSeparator()
		toolApplyShutdown = self.toolbar8.AddTool(806, _('Apply'), wx.Bitmap(self.currentdir+"/data/apply.png"))
		self.Bind(wx.EVT_TOOL, self.onToolApplyShutdown, toolApplyShutdown)

		self.toolbar9 = wx.ToolBar(self.raspSettings, style=wx.TB_TEXT)
		toolPoweroff = self.toolbar9.AddCheckTool(901, _('Power off'), wx.Bitmap(self.currentdir+"/data/poweroff.png"))
		self.Bind(wx.EVT_TOOL, self.onToolPoweroff, toolPoweroff)
		separatorLabel1 = wx.StaticText(self.toolbar9, 906, label='    ')
		toolSeparatorLabel1 = self.toolbar9.AddControl(separatorLabel1)
		self.gpioPoweroff = wx.TextCtrl(self.toolbar9, 902, style=wx.CB_READONLY)
		toolGpioPoweroff = self.toolbar9.AddControl(self.gpioPoweroff)
		toolSetGpioPoweroff = self.toolbar9.AddTool(903, _('GPIO'), wx.Bitmap(self.currentdir+"/data/chip.png"))
		self.Bind(wx.EVT_TOOL, self.onToolSetGpioPoweroff, toolSetGpioPoweroff)
		self.transitionPoweroff = wx.ComboBox(self.toolbar9, 904, _('Transition'), choices=[_('low->high'),_('high->low')], size=(150,-1), style=wx.CB_DROPDOWN)
		toolTransitionPoweroff= self.toolbar9.AddControl(self.transitionPoweroff)	
		self.toolbar9.AddSeparator()
		toolApplyPoweroff = self.toolbar9.AddTool(905, _('Apply'), wx.Bitmap(self.currentdir+"/data/apply.png"))
		self.Bind(wx.EVT_TOOL, self.onToolApplyPoweroff, toolApplyPoweroff)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.toolbar5, 0, wx.EXPAND, 0)
		sizer.Add(powerLabel, 0, wx.ALL | wx.EXPAND, 10)
		sizer.Add(self.toolbar8, 0, wx.EXPAND, 0)
		sizer.Add(self.toolbar9, 0, wx.EXPAND, 0)
		self.raspSettings.SetSizer(sizer)

		if self.platform.isRPI:

			backlightPath = "/sys/class/backlight"
			backlightDevices = os.listdir(backlightPath)
			if backlightDevices: 
				if os.path.exists('/usr/share/applications/openplotter-brightness.desktop'):
					self.toolbar5.ToggleTool(504,True)
					self.toolbar5.EnableTool(505,True)
				else:
					self.toolbar5.ToggleTool(504,False)
					self.toolbar5.EnableTool(505,False)
			else:
				self.toolbar5.EnableTool(504,False)
				self.toolbar5.EnableTool(505,False)

			out = subprocess.check_output('echo $XDG_SESSION_TYPE', shell=True).decode(sys.stdin.encoding)
			if 'wayland' in out: self.toolbar5.ToggleTool(506,True)

			try:
				subprocess.check_output(['systemctl', 'is-enabled', 'create_ap_interface.service']).decode(sys.stdin.encoding)
				self.toolbar5.ToggleTool(507,True)
			except: pass

			try: shutdown = eval(self.conf.get('GENERAL', 'shutdown'))
			except: shutdown = {}
			if shutdown:
				self.gpioShutdown.SetValue(shutdown['gpio'])
				self.transitionShutdown.SetSelection(shutdown['transition'])
				self.gpioPullShutdown.SetSelection(shutdown['pull'])

			try: poweroff = eval(self.conf.get('GENERAL', 'poweroff'))
			except: poweroff = {}
			if poweroff:
				self.gpioPoweroff.SetValue(poweroff['gpio'])
				self.transitionPoweroff.SetSelection(poweroff['transition'])

			try: config = open('/boot/firmware/config.txt', 'r')
			except: config = open('/boot/config.txt', 'r')
			data = config.read()
			config.close()
			if 'dtoverlay=gpio-poweroff' in data and not '#dtoverlay=gpio-poweroff' in data: self.toolbar9.ToggleTool(901,True)
			else: 
				self.toolbar9.ToggleTool(901,False)
				self.disablePowerOff()

			if 'dtoverlay=gpio-shutdown' in data and not '#dtoverlay=gpio-shutdown' in data: self.toolbar8.ToggleTool(801,True)
			else: 
				self.toolbar8.ToggleTool(801,False)
				self.disableShutdown()
		else: 
			self.toolbar5.EnableTool(503,False)
			self.toolbar5.EnableTool(504,False)
			self.toolbar5.EnableTool(505,False)
			self.toolbar5.EnableTool(506,False)
			self.toolbar8.EnableTool(801,False)
			self.toolbar8.EnableTool(806,False)
			self.toolbar9.EnableTool(901,False)
			self.toolbar9.EnableTool(905,False)
			self.disablePowerOff()
			self.disableShutdown()

	def disablePowerOff(self):
		self.toolbar9.EnableTool(902,False)
		self.toolbar9.EnableTool(903,False)
		self.toolbar9.EnableTool(904,False)

	def disableShutdown(self):
		self.toolbar8.EnableTool(802,False)
		self.toolbar8.EnableTool(803,False)
		self.toolbar8.EnableTool(804,False)
		self.toolbar8.EnableTool(805,False)

	def enablePowerOff(self):
		self.toolbar9.EnableTool(902,True)
		self.toolbar9.EnableTool(903,True)
		self.toolbar9.EnableTool(904,True)

	def enableShutdown(self):
		self.toolbar8.EnableTool(802,True)
		self.toolbar8.EnableTool(803,True)
		self.toolbar8.EnableTool(804,True)
		self.toolbar8.EnableTool(805,True)

	def onToolShutdown(self,e):
		if self.toolbar8.GetToolState(801):
			self.enableShutdown()
		else:
			self.disableShutdown()

	def onToolSetGpioShutdown(self,e):
		gpioPin = '0'
		gpioBCM = self.gpioShutdown.GetValue()
		if gpioBCM:
			gpioBCM = 'GPIO '+gpioBCM
			gpios = Gpio()
			for i in gpios.gpioMap:
				if gpioBCM == i['BCM']: gpioPin = i['physical']
		dlg = GpioMap(['GPIO'],gpioPin)
		res = dlg.ShowModal()
		if res == wx.ID_OK:
			gpioBCM = dlg.selected['BCM'].replace('GPIO ','')
			self.gpioShutdown.SetValue(gpioBCM)
		dlg.Destroy()

	def onToolApplyShutdown(self,e):
		if self.toolbar8.GetToolState(801):
			if not self.gpioShutdown.GetValue():
				self.ShowStatusBarRED(_('Failed, you need to set a GPIO'))
				return
			else: gpio = self.gpioShutdown.GetValue()
			if self.transitionShutdown.GetSelection() == -1:
				self.ShowStatusBarRED(_('Failed, you need to set a transition mode'))
				return
			else: transition = self.transitionShutdown.GetSelection()
			if self.gpioPullShutdown.GetSelection() == -1:
				self.ShowStatusBarRED(_('Failed, you need to set a GPIO pull mode'))
				return
			else: pull = self.gpioPullShutdown.GetSelection()
			data = {'gpio':gpio, 'transition':transition,'pull':pull}
			self.conf.set('GENERAL', 'shutdown', str(data))
			if pull == 0: pull = 'up'
			elif pull == 1: pull = 'down'
			elif pull == 2: pull = 'off'
			overlay = 'dtoverlay=gpio-shutdown,gpio_pin='+gpio+',active_low='+str(transition)+',gpio_pull='+pull+'\n'
		else: 
			self.conf.set('GENERAL', 'shutdown', '')
			overlay = ''
		subprocess.call([self.platform.admin, 'python3', self.currentdir+'/service.py', 'shutdown', overlay])
		self.ShowStatusBarGREEN(_('Done. Changes will be applied after the next reboot'))

	def onToolPoweroff(self,e):
		if self.toolbar9.GetToolState(901):
			self.enablePowerOff()
		else:
			self.disablePowerOff()

	def onToolSetGpioPoweroff(self,e):
		gpioPin = '0'
		gpioBCM = self.gpioPoweroff.GetValue()
		if gpioBCM:
			gpioBCM = 'GPIO '+gpioBCM
			gpios = Gpio()
			for i in gpios.gpioMap:
				if gpioBCM == i['BCM']: gpioPin = i['physical']
		dlg = GpioMap(['GPIO'],gpioPin)
		res = dlg.ShowModal()
		if res == wx.ID_OK:
			gpioBCM = dlg.selected['BCM'].replace('GPIO ','')
			self.gpioPoweroff.SetValue(gpioBCM)
		dlg.Destroy()

	def onToolApplyPoweroff(self,e):
		if self.toolbar9.GetToolState(901):
			if not self.gpioPoweroff.GetValue():
				self.ShowStatusBarRED(_('Failed, you need to set a GPIO'))
				return
			else: gpio = self.gpioPoweroff.GetValue()
			if self.transitionPoweroff.GetSelection() == -1:
				self.ShowStatusBarRED(_('Failed, you need to set a transition mode'))
				return
			else: transition = self.transitionPoweroff.GetSelection()
			data = {'gpio':gpio, 'transition':transition}
			self.conf.set('GENERAL', 'poweroff', str(data))
			overlay = 'dtoverlay=gpio-poweroff,gpiopin='+gpio+',active_low='+str(transition)+'\n'
		else: 
			self.conf.set('GENERAL', 'poweroff', '')
			overlay = ''
		subprocess.call([self.platform.admin, 'python3', self.currentdir+'/service.py', 'poweroff', overlay])
		self.ShowStatusBarGREEN(_('Done. Changes will be applied after the next reboot'))

	def OnToolbacklightInstall(self,e):
		if self.toolbar5.GetToolState(504):
			self.ShowStatusBarYELLOW(_('Installing rpi-backlight, please wait...'))
			msg = _('rpi-backlight will be installed.\n')
			msg += _('Are you sure?')
			dlg = wx.MessageDialog(None, msg, _('Question'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
			if dlg.ShowModal() == wx.ID_YES: 
				self.toolbar5.EnableTool(505,True)
				subprocess.call([self.platform.admin, 'python3', self.currentdir+'/backlight.py', 'install'])
				self.ShowStatusBarGREEN(_('rpi-backlight installed'))
			else:
				self.toolbar5.ToggleTool(504,False)
				self.toolbar5.EnableTool(505,False)
				self.ShowStatusBarRED(_('Installation canceled'))
		else:
			self.ShowStatusBarYELLOW(_('Uninstalling rpi-backlight, please wait...'))
			msg = _('rpi-backlight will be uninstalled.\n')
			msg += _('Are you sure?')
			dlg = wx.MessageDialog(None, msg, _('Question'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
			if dlg.ShowModal() == wx.ID_YES: 
				self.toolbar5.EnableTool(505,False)
				subprocess.call([self.platform.admin, 'python3', self.currentdir+'/backlight.py', 'uninstall'])
				self.ShowStatusBarGREEN(_('rpi-backlight uninstalled'))
			else:
				self.toolbar5.ToggleTool(504,True)
				self.toolbar5.EnableTool(505,True)
				self.ShowStatusBarRED(_('Uninstallation canceled'))
		dlg.Destroy()

	def OnToolbacklightSet(self,e):
			subprocess.Popen('openplotter-backlight-gui')

	def OnToolWayland(self,e):
		if self.toolbar5.GetToolState(506):
			msg = _('Wayland will be enabled and X11 disabled. Some programs may not yet work correctly for Wayland.')
			msg += _('\n')
			msg += _('OpenPlotter will reboot. Are you sure?')
			dlg = wx.MessageDialog(None, msg, _('Question'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
			if dlg.ShowModal() == wx.ID_YES: 
				subprocess.call([self.platform.admin, 'python3', self.currentdir+'/wayland.py', 'W2'])
				out = subprocess.check_output('raspi-config nonint get_vnc', shell=True).decode(sys.stdin.encoding)
				if '0' in out: self.conf.set('GENERAL', 'forceVNC', '1')
				os.system('shutdown -r now')
			else:
				self.toolbar5.ToggleTool(506,False)
				self.ShowStatusBarRED(_('Canceled'))
		else:
			msg = _('Wayland will be disabled and X11 enabled.')
			msg += _('\n')
			msg += _('OpenPlotter will reboot. Are you sure?')
			dlg = wx.MessageDialog(None, msg, _('Question'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
			if dlg.ShowModal() == wx.ID_YES: 
				subprocess.call([self.platform.admin, 'python3', self.currentdir+'/wayland.py', 'W1'])
				out = subprocess.check_output('raspi-config nonint get_vnc', shell=True).decode(sys.stdin.encoding)
				if '0' in out: self.conf.set('GENERAL', 'forceVNC', '1')
				os.system('shutdown -r now')
			else:
				self.toolbar5.ToggleTool(506,True)
				self.ShowStatusBarRED(_('Canceled'))
		dlg.Destroy()

	def OnToolHotspot(self,e):
		if self.toolbar5.GetToolState(507):
			msg = _('A dual Hotspot/Client connection will be created. Do not forget to change the default Hotspot password "12345678" if you have not already.')
			msg += _('\n')
			msg += _('OpenPlotter will reboot. Are you sure?')
			dlg = wx.MessageDialog(None, msg, _('Question'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
			if dlg.ShowModal() == wx.ID_YES:
				pass
				subprocess.call([self.platform.admin, 'openplotter-ap', 'enable'])
				os.system('shutdown -r now')
			else:
				self.toolbar5.ToggleTool(507,False)
				self.ShowStatusBarRED(_('Canceled'))
		else:
			msg = _('The dual Hotspot/Client connection will be disabled and only the Client connection will be able to be established.')
			msg += _('\n')
			msg += _('OpenPlotter will reboot. Are you sure?')
			dlg = wx.MessageDialog(None, msg, _('Question'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
			if dlg.ShowModal() == wx.ID_YES:
				pass
				subprocess.call([self.platform.admin, 'openplotter-ap', 'disable'])
				os.system('shutdown -r now')
			else:
				self.toolbar5.ToggleTool(507,True)
				self.ShowStatusBarRED(_('Canceled'))
		dlg.Destroy()

	def OnToolGpio(self,e):
		dlg = GpioMap()
		res = dlg.ShowModal()
		dlg.Destroy()

	###################################################################################

	def pageApps(self):
		self.listApps = wx.ListCtrl(self.apps, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES, size=(-1,200))
		self.listApps.InsertColumn(0, _('Name'), width=220)
		self.listApps.InsertColumn(1, _('Installed'), width=120)
		self.listApps.InsertColumn(2, _('Candidate'), width=120)
		self.listApps.InsertColumn(3, _('Pending tasks'), width=180)
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
		self.notebook.ChangeSelection(3)
		self.ShowStatusBarYELLOW(_('Updating packages data, please wait... '))
		command = self.platform.admin+' apt update'
		popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
		for line in popen.stdout:
			if not 'Warning' in line and not 'WARNING' in line:
				self.logger.WriteText(line)
				self.logger.ShowPosition(self.logger.GetLastPosition())
				wx.GetApp().Yield()
		self.OnRefreshButton()

	def OnToolSources(self, e):
		self.logger.Clear()
		self.notebook.ChangeSelection(3)
		self.ShowStatusBarYELLOW(_('Adding packages sources, please wait... '))
		command = self.platform.admin+' settingsSourcesInstall'
		popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
		for line in popen.stdout:
			if not 'Warning' in line and not 'WARNING' in line:
				self.logger.WriteText(line)
				self.logger.ShowPosition(self.logger.GetLastPosition())
				wx.GetApp().Yield()
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
			self.notebook.ChangeSelection(3)
			self.ShowStatusBarYELLOW(_('Installing package, please wait... '))
			command = self.platform.admin+' apt install -y '+package
			popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
			for line in popen.stdout:
				if not 'Warning' in line and not 'WARNING' in line:
					self.logger.WriteText(line)
					self.logger.ShowPosition(self.logger.GetLastPosition())
					wx.GetApp().Yield()
			postInstall = apps[index]['postInstall']
			if postInstall:
				self.ShowStatusBarYELLOW(_('Running post-installation scripts, please wait... '))
				popen = subprocess.Popen(postInstall, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
				for line in popen.stdout:
					if not 'Warning' in line and not 'WARNING' in line:
						self.logger.WriteText(line)
						self.logger.ShowPosition(self.logger.GetLastPosition())
						wx.GetApp().Yield()
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
			self.notebook.ChangeSelection(3)
			preUninstall = apps[index]['preUninstall']
			if preUninstall:
				self.ShowStatusBarYELLOW(_('Running pre-uninstall scripts, please wait... '))
				popen = subprocess.Popen(preUninstall, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
				for line in popen.stdout:
					if not 'Warning' in line and not 'WARNING' in line:
						self.logger.WriteText(line)
						self.logger.ShowPosition(self.logger.GetLastPosition())
						wx.GetApp().Yield()
			self.ShowStatusBarYELLOW(_('Uninstalling packages, please wait... '))
			command = self.platform.admin+' apt autoremove -y '+package
			popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
			for line in popen.stdout:
				if not 'Warning' in line and not 'WARNING' in line:
					self.logger.WriteText(line)
					self.logger.ShowPosition(self.logger.GetLastPosition())
					wx.GetApp().Yield()
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
		self.notebook.ChangeSelection(3)
		self.ShowStatusBarYELLOW(_('Reading changelog, please wait... '))
		command = 'apt changelog '+apps[index]['package']
		popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
		for line in popen.stdout:
			if not 'Warning' in line and not 'WARNING' in line:
				self.logger.WriteText(line)
				wx.GetApp().Yield()
		self.ShowStatusBarGREEN(_('Done'))

	def readApps(self):
		self.notebook.ChangeSelection(0)
		self.listApps.DeleteAllItems()
		self.ShowStatusBarYELLOW(_('Checking apps list, please wait... '))
		wx.GetApp().Yield()
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
			self.ShowStatusBarYELLOW(_('Checking apps list, please wait... '))
			wx.GetApp().Yield()

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

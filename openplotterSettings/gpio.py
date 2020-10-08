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

import importlib, wx, os
from .conf import Conf
from .language import Language
from .appsList import AppsList
import wx.richtext as rt

class Gpio:
	def __init__(self):
		self.conf = Conf()
		self.currentdir = os.path.dirname(os.path.abspath(__file__))
		self.currentLanguage = self.conf.get('GENERAL', 'lang')
		self.language = Language(self.currentdir,'openplotter-settings',self.currentLanguage)

		self.gpioMap = [
			{'physical':'1', 'BCM': '3v3', 'feature': _('Power'), 'shared': True, 'usedBy': []},
			{'physical':'2', 'BCM': '5v', 'feature': _('Power'), 'shared': True, 'usedBy': []},
			{'physical':'3', 'BCM': 'GPIO 2', 'feature': 'I2C', 'shared': True, 'usedBy': []},
			{'physical':'4', 'BCM': '5v', 'feature': _('Power'), 'shared': True, 'usedBy': []},
			{'physical':'5', 'BCM': 'GPIO 3', 'feature': 'I2C', 'shared': True, 'usedBy': []},
			{'physical':'6', 'BCM': _('Ground'), 'feature': _('Power'), 'shared': True, 'usedBy': []},
			{'physical':'7', 'BCM': 'GPIO 4', 'feature': 'GPIO', 'shared': False, 'usedBy': []},
			{'physical':'8', 'BCM': 'GPIO 14', 'feature': 'UART', 'shared': False, 'usedBy': []},
			{'physical':'9', 'BCM': _('Ground'), 'feature': _('Power'), 'shared': True, 'usedBy': []},
			{'physical':'10', 'BCM': 'GPIO 15', 'feature': 'UART', 'shared': False, 'usedBy': []},
			{'physical':'11', 'BCM': 'GPIO 17', 'feature': 'GPIO', 'shared': False, 'usedBy': []},
			{'physical':'12', 'BCM': 'GPIO 18', 'feature': 'GPIO', 'shared': False, 'usedBy': []},
			{'physical':'13', 'BCM': 'GPIO 27', 'feature': 'GPIO', 'shared': False, 'usedBy': []},
			{'physical':'14', 'BCM': _('Ground'), 'feature': _('Power'), 'shared': True, 'usedBy': []},
			{'physical':'15', 'BCM': 'GPIO 22', 'feature': 'GPIO', 'shared': False, 'usedBy': []},
			{'physical':'16', 'BCM': 'GPIO 23', 'feature': 'GPIO', 'shared': False, 'usedBy': []},
			{'physical':'17', 'BCM': '3v3', 'feature': _('Power'), 'shared': True, 'usedBy': []},
			{'physical':'18', 'BCM': 'GPIO 24', 'feature': 'GPIO', 'shared': False, 'usedBy': []},
			{'physical':'19', 'BCM': 'GPIO 10', 'feature': 'SPI', 'shared': True, 'usedBy': []},
			{'physical':'20', 'BCM': _('Ground'), 'feature': _('Power'), 'shared': True, 'usedBy': []},
			{'physical':'21', 'BCM': 'GPIO 9', 'feature': 'SPI', 'shared': True, 'usedBy': []},
			{'physical':'22', 'BCM': 'GPIO 25', 'feature': 'GPIO', 'shared': False, 'usedBy': []},
			{'physical':'23', 'BCM': 'GPIO 11', 'feature': 'SPI', 'shared': True, 'usedBy': []},
			{'physical':'24', 'BCM': 'GPIO 8', 'feature': 'SPI', 'shared': False, 'usedBy': []},
			{'physical':'25', 'BCM': _('Ground'), 'feature': _('Power'), 'shared': True, 'usedBy': []},
			{'physical':'26', 'BCM': 'GPIO 7', 'feature': 'SPI', 'shared': False, 'usedBy': []},
			{'physical':'27', 'BCM': 'GPIO 0', 'feature': 'EEPROM', 'shared': False, 'usedBy': []},
			{'physical':'28', 'BCM': 'GPIO 1', 'feature': 'EEPROM', 'shared': False, 'usedBy': []},
			{'physical':'29', 'BCM': 'GPIO 5', 'feature': 'GPIO', 'shared': False, 'usedBy': []},
			{'physical':'30', 'BCM': _('Ground'), 'feature': _('Power'), 'shared': True, 'usedBy': []},
			{'physical':'31', 'BCM': 'GPIO 6', 'feature': 'GPIO', 'shared': False, 'usedBy': []},
			{'physical':'32', 'BCM': 'GPIO 12', 'feature': 'GPIO', 'shared': False, 'usedBy': []},
			{'physical':'33', 'BCM': 'GPIO 13', 'feature': 'GPIO', 'shared': False, 'usedBy': []},
			{'physical':'34', 'BCM': _('Ground'), 'feature': _('Power'), 'shared': True, 'usedBy': []},
			{'physical':'35', 'BCM': 'GPIO 19', 'feature': 'GPIO', 'shared': False, 'usedBy': []},
			{'physical':'36', 'BCM': 'GPIO 16', 'feature': 'GPIO', 'shared': False, 'usedBy': []},
			{'physical':'37', 'BCM': 'GPIO 26', 'feature': 'GPIO', 'shared': False, 'usedBy': []},
			{'physical':'38', 'BCM': 'GPIO 20', 'feature': 'GPIO', 'shared': False, 'usedBy': []},
			{'physical':'39', 'BCM': _('Ground'), 'feature': _('Power'), 'shared': True, 'usedBy': []},
			{'physical':'40', 'BCM': 'GPIO 21', 'feature': 'GPIO', 'shared': False, 'usedBy': []}
		] 

		UsedGpios = []
		appsList = AppsList()
		appsDict = appsList.appsDict
		for i in appsDict:
			name = i['module']
			if name:
				gpio = False
				try:
					gpio = importlib.import_module(name+'.gpio')
					if gpio:
						target = gpio.Gpio(self.conf)
						targetGpios = target.usedGpios()
						if targetGpios:
							for i in targetGpios:
								UsedGpios.append(i)
				except Exception as e: print(str(e))

		for i in UsedGpios:
			for ii in self.gpioMap:
				if i['physical'] == ii['physical']:
					ii['usedBy'].append({'app': i['app'], 'id': i['id']})

#################################################

class GpioMap(wx.Dialog):
	def __init__(self, allowed='0', edit='0'):
		self.conf = Conf()
		self.allowed = allowed
		self.edit = edit
		self.currentdir = os.path.dirname(os.path.abspath(__file__))
		self.currentLanguage = self.conf.get('GENERAL', 'lang')
		self.language = Language(self.currentdir,'openplotter-settings',self.currentLanguage)

		self.gpio = Gpio()
		self.gpioMap = self.gpio.gpioMap

		if self.allowed != '0': title = _('Select GPIO')
		else: title = _('GPIO Map')

		wx.Dialog.__init__(self, None, title=title, size=(600,460))
		self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		panel = wx.Panel(self)

		self.pin1 = wx.CheckBox(panel, 1, style=wx.ALIGN_RIGHT)
		self.pin3 = wx.CheckBox(panel, 3, style=wx.ALIGN_RIGHT)
		self.pin5 = wx.CheckBox(panel, 5, style=wx.ALIGN_RIGHT)
		self.pin7 = wx.CheckBox(panel, 7, style=wx.ALIGN_RIGHT)
		self.pin9 = wx.CheckBox(panel, 9, style=wx.ALIGN_RIGHT)
		self.pin11 = wx.CheckBox(panel, 11, style=wx.ALIGN_RIGHT)
		self.pin13 = wx.CheckBox(panel, 13, style=wx.ALIGN_RIGHT)
		self.pin15 = wx.CheckBox(panel, 15, style=wx.ALIGN_RIGHT)
		self.pin17 = wx.CheckBox(panel, 17, style=wx.ALIGN_RIGHT)
		self.pin19 = wx.CheckBox(panel, 19, style=wx.ALIGN_RIGHT)
		self.pin21 = wx.CheckBox(panel, 21, style=wx.ALIGN_RIGHT)
		self.pin23 = wx.CheckBox(panel, 23, style=wx.ALIGN_RIGHT)
		self.pin25 = wx.CheckBox(panel, 25, style=wx.ALIGN_RIGHT)
		self.pin27 = wx.CheckBox(panel, 27, style=wx.ALIGN_RIGHT)
		self.pin29 = wx.CheckBox(panel, 29, style=wx.ALIGN_RIGHT)
		self.pin31 = wx.CheckBox(panel, 31, style=wx.ALIGN_RIGHT)
		self.pin33 = wx.CheckBox(panel, 33, style=wx.ALIGN_RIGHT)
		self.pin35 = wx.CheckBox(panel, 35, style=wx.ALIGN_RIGHT)
		self.pin37 = wx.CheckBox(panel, 37, style=wx.ALIGN_RIGHT)
		self.pin39 = wx.CheckBox(panel, 39, style=wx.ALIGN_RIGHT)

		self.pin2 = wx.CheckBox(panel, 2, style=wx.ALIGN_LEFT)
		self.pin4 = wx.CheckBox(panel, 4, style=wx.ALIGN_LEFT)
		self.pin6 = wx.CheckBox(panel, 6, style=wx.ALIGN_LEFT)
		self.pin8 = wx.CheckBox(panel, 8, style=wx.ALIGN_LEFT)
		self.pin10 = wx.CheckBox(panel, 10, style=wx.ALIGN_LEFT)
		self.pin12 = wx.CheckBox(panel, 12, style=wx.ALIGN_LEFT)
		self.pin14 = wx.CheckBox(panel, 14, style=wx.ALIGN_LEFT)
		self.pin16 = wx.CheckBox(panel, 16, style=wx.ALIGN_LEFT)
		self.pin18 = wx.CheckBox(panel, 18, style=wx.ALIGN_LEFT)
		self.pin20 = wx.CheckBox(panel, 20, style=wx.ALIGN_LEFT)
		self.pin22 = wx.CheckBox(panel, 22, style=wx.ALIGN_LEFT)
		self.pin24 = wx.CheckBox(panel, 24, style=wx.ALIGN_LEFT)
		self.pin26 = wx.CheckBox(panel, 26, style=wx.ALIGN_LEFT)
		self.pin28 = wx.CheckBox(panel, 28, style=wx.ALIGN_LEFT)
		self.pin30 = wx.CheckBox(panel, 30, style=wx.ALIGN_LEFT)
		self.pin32 = wx.CheckBox(panel, 32, style=wx.ALIGN_LEFT)
		self.pin34 = wx.CheckBox(panel, 34, style=wx.ALIGN_LEFT)
		self.pin36 = wx.CheckBox(panel, 36, style=wx.ALIGN_LEFT)
		self.pin38 = wx.CheckBox(panel, 38, style=wx.ALIGN_LEFT)
		self.pin40 = wx.CheckBox(panel, 40, style=wx.ALIGN_LEFT)
		self.Bind(wx.EVT_CHECKBOX,self.onChecked)

		self.logger = rt.RichTextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_DONTWRAP|wx.LC_SORT_ASCENDING)
		self.logger.SetMargins((10,10))

		if self.allowed != '0':
			cancelBtn = wx.Button(panel, wx.ID_CANCEL)
			self.okBtn = wx.Button(panel, wx.ID_OK)

		left = wx.BoxSizer(wx.VERTICAL)
		left.AddSpacer(6)
		left.Add(self.pin1, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin3, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin5, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin7, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin9, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin11, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin13, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin15, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin17, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin19, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin21, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin23, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin25, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin27, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin29, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin31, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin33, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin35, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin37, 0, wx.ALIGN_RIGHT, 0)
		left.AddSpacer(4)
		left.Add(self.pin39, 0, wx.ALIGN_RIGHT, 0)

		right = wx.BoxSizer(wx.VERTICAL)
		right.AddSpacer(4)
		right.Add(self.pin2, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin4, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin6, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin8, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin10, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin12, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin14, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin16, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin18, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin20, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin22, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin24, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin26, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin28, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin30, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin32, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin34, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin36, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin38, 0, wx.ALIGN_LEFT, 0)
		right.Add(self.pin40, 0, wx.ALIGN_LEFT, 0)

		right2 = wx.BoxSizer(wx.VERTICAL)
		right2.Add(self.logger, 1, wx.ALL | wx.EXPAND, 5)
		if self.allowed != '0':
			right2.Add(self.okBtn, 0, wx.ALL | wx.EXPAND, 5)
			right2.Add(cancelBtn, 0, wx.ALL | wx.EXPAND, 5)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(left, 0, wx.ALL, 0)
		hbox.Add(right, 0, wx.ALL, 0)
		hbox.Add(right2, 1, wx.ALL | wx.EXPAND, 5)

		panel.SetSizer(hbox)
		self.Centre() 

		self.refresh()

	def refresh(self):
		for i in range(1,41): 
			if i % 2 != 0:
				if not 'GPIO' in self.gpioMap[i-1]['feature']:
					label = '('+self.gpioMap[i-1]['feature']+') '+self.gpioMap[i-1]['BCM']+' - '+self.gpioMap[i-1]['physical']
				else:
					label = self.gpioMap[i-1]['BCM']+' - '+self.gpioMap[i-1]['physical']
			else:
				label = self.gpioMap[i-1]['physical']+' - '+self.gpioMap[i-1]['BCM']
				if not 'GPIO' in self.gpioMap[i-1]['feature']: 
					label += ' ('+self.gpioMap[i-1]['feature']+')'

			if i < 41: eval('self.pin'+str(i)).SetLabel(label)

			if len(self.gpioMap[i-1]['usedBy']) > 0:
				eval('self.pin'+str(i)).SetForegroundColour((0, 130, 0))
				if not self.gpioMap[i-1]['shared']:
					if len(self.gpioMap[i-1]['usedBy']) > 1:
						eval('self.pin'+str(i)).SetForegroundColour((130, 0, 0))
		if self.edit != '0':
			try: eval('self.pin'+self.edit).SetValue(True)
			except: pass

	def onChecked(self, e): 
		selected = e.GetEventObject()
		for i in range(1,41): 
			if i < 41: eval('self.pin'+str(i)).SetValue(False)
		selected.SetValue(True)
		pin = self.gpioMap[selected.GetId()-1]
		self.logger.Clear()
		self.logger.BeginTextColour((55, 55, 55))
		self.logger.BeginBold()
		self.logger.WriteText(_('Physical pin'))
		self.logger.EndBold()
		self.logger.WriteText(': '+pin['physical'])
		self.logger.Newline()
		self.logger.BeginBold()
		self.logger.WriteText(_('BCM name'))
		self.logger.EndBold()
		self.logger.WriteText(': '+pin['BCM'])
		self.logger.Newline()
		self.logger.BeginBold()
		self.logger.WriteText(_('Interface'))
		self.logger.EndBold()
		self.logger.WriteText(': '+pin['feature'])
		self.logger.Newline()
		self.logger.BeginBold()
		self.logger.WriteText(_('Shared'))
		self.logger.EndBold()
		if pin['shared']:
			self.logger.WriteText(': '+_('Yes'))
		else:
			self.logger.WriteText(': '+_('No'))		
		self.logger.Newline()
		if pin['usedBy']:
			self.logger.BeginBold()
			self.logger.WriteText(_('Used by'))
			self.logger.EndBold()
			self.logger.WriteText(': ')
			usedBy = ''
			for i in pin['usedBy']:
				if usedBy: usedBy += ', '
				usedBy += i['app']+' - '+i['id']
			self.logger.WriteText(usedBy)
			self.logger.Newline()
		self.logger.Newline()

		if len(pin['usedBy']) > 1:
			if not pin['shared']:
				self.logger.BeginTextColour((130, 0, 0))
				self.logger.WriteText(_('There is a conflict with this GPIO.'))
				self.logger.EndTextColour()
				self.logger.Newline()

		if self.allowed != '0':
			if len(pin['usedBy']) > 0:
				if not pin['shared']:
					self.okBtn.Disable()
					self.selected = False
					self.logger.BeginTextColour((55, 55, 55))
					self.logger.WriteText(_('You can not select this GPIO to do this job.'))
					self.logger.EndTextColour()
					return

			if pin['feature'] in self.allowed:
				self.selected = pin
				self.okBtn.Enable()	
			else:
				self.okBtn.Disable()
				self.selected = False
				self.logger.BeginTextColour((55, 55, 55))
				self.logger.WriteText(_('You can not select this GPIO to do this job.'))
				self.logger.EndTextColour()


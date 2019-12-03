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

import wx, pyudev

class Serial(wx.Dialog):
	def __init__(self):
		context = pyudev.Context()
		self.devices = []
		for i in context.list_devices(subsystem='tty'):
			#for tag in device:
				#print (tag+': '+device.get(tag))
			DEVNAME = i.get('DEVNAME')
			DEVPATH = i.get('DEVPATH')
			if not '/virtual/' in DEVPATH or 'moitessier' in DEVNAME: self.devices.append(i)

class AddPort(wx.Dialog):
	def __init__(self):
		wx.Dialog.__init__(self, None, title=_('Add Serial Port'), size=(-1,200))
		panel = wx.Panel(self)

		serial = Serial()
		devices = serial.devices
		self.listDevices = []
		for device in devices:
			self.listDevices.append(device.get('DEVNAME'))
			if 'DEVLINKS' in device:
				i = device.get('DEVLINKS').split(' ')
				for ii in i:
					if 'ttyOP' in ii: self.listDevices.append(ii)

		OPserial = False
		self.listDevicesOP = []

		for device in self.listDevices:
			if 'ttyOP' in device:
				self.listDevicesOP.append(device)
				OPserial = True

		if OPserial:
			self.port = wx.Choice(panel, choices=self.listDevicesOP)
			self.OPserialTrue = wx.CheckBox(panel, label=_('Show only Openplotter-Serial managed ports'))
			self.OPserialTrue.Bind(wx.EVT_CHECKBOX, self.on_OPserialTrue)
			self.OPserialTrue.SetValue(True)
		else:
			self.port = wx.Choice(panel, choices=self.listDevices)

		cancelBtn = wx.Button(panel, wx.ID_CANCEL)
		okBtn = wx.Button(panel, wx.ID_OK)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(cancelBtn, 1, wx.ALL | wx.EXPAND, 10)
		hbox.Add(okBtn, 1, wx.ALL | wx.EXPAND, 10)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.port, 0, wx.ALL | wx.EXPAND, 10)
		if OPserial:
			vbox.Add(self.OPserialTrue, 0, wx.ALL | wx.EXPAND, 10)
		vbox.AddStretchSpacer(1)
		vbox.Add(hbox, 0, wx.EXPAND, 0)

		panel.SetSizer(vbox)
		self.Centre() 

	def on_OPserialTrue(self,e):
		self.port.Clear()
		if self.OPserialTrue.GetValue():
			self.port.AppendItems(self.listDevicesOP)
		else:
			self.port.AppendItems(self.listDevices)	
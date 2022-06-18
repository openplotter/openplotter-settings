#!/usr/bin/env python3

# This file is part of OpenPlotter.
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

import wx, pyudev, sys, subprocess

class Serial(wx.Dialog):
	def __init__(self):
		context = pyudev.Context()
		self.devices = []
		for i in context.list_devices(subsystem='tty'):
			DEVNAME = i.get('DEVNAME')
			DEVPATH = i.get('DEVPATH')
			try:
				subprocess.check_output(['systemctl', 'is-active', 'bluetooth']).decode(sys.stdin.encoding)
				btStatus = True
			except: btStatus = False
			if not '/virtual/' in DEVPATH or 'moitessier' in DEVNAME:
				if not '/devices/platform/serial' in DEVPATH:
					if 'ttyAMA0' in DEVPATH and btStatus: pass
					else: self.devices.append(i)
			'''
			if not '/devices/virtual/tty/tty' in DEVPATH:
				for tag in i:
					print (tag+': '+i.get(tag))
					print('-------------------------------------')
				print('############################################')
			'''

class AddPort(wx.Dialog):
	def __init__(self, deviceSent, deviceStatus, baudsSent, baudsStatus):
		wx.Dialog.__init__(self, None, title=_('Add serial device'), size=(-1,230))
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
			self.port = wx.ComboBox(panel, choices=self.listDevicesOP)
			self.OPserialTrue = wx.CheckBox(panel, label=_('Show only Openplotter-Serial managed ports'))
			self.OPserialTrue.Bind(wx.EVT_CHECKBOX, self.on_OPserialTrue)
			self.OPserialTrue.SetValue(True)
		else:
			self.port = wx.ComboBox(panel, choices=self.listDevices)

		baudsList = ['4800', '9600', '19200', '38400', '57600', '115200', '230400', '460800', '921600']
		baudsLabel = wx.StaticText(panel, label=_('Baud Rate: '))
		self.bauds = wx.ComboBox(panel, choices=baudsList)

		if deviceSent: self.port.SetValue(deviceSent)
		else: self.port.SetValue('')
		if not deviceStatus: self.port.Disable()
		if baudsSent: self.bauds.SetValue(baudsSent)
		else: self.bauds.SetValue('')
		if not baudsStatus: self.bauds.Disable()

		cancelBtn = wx.Button(panel, wx.ID_CANCEL)
		okBtn = wx.Button(panel, wx.ID_OK)

		hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		hbox3.Add(baudsLabel, 0, wx.RIGHT | wx.LEFT | wx.EXPAND, 10)
		hbox3.Add(self.bauds, 1, wx.RIGHT | wx.LEFT | wx.EXPAND, 10)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(cancelBtn, 1, wx.ALL | wx.EXPAND, 10)
		hbox.Add(okBtn, 1, wx.ALL | wx.EXPAND, 10)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.port, 0, wx.ALL | wx.EXPAND, 10)
		if OPserial:
			vbox.Add(self.OPserialTrue, 0, wx.RIGHT | wx.LEFT | wx.EXPAND, 10)
			vbox.AddSpacer(10)
		vbox.Add(hbox3, 0, wx.EXPAND, 0)
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
		self.port.SetValue('')
		
'''
class AddNetworkConnection(wx.Dialog):
	def __init__(self, data, dataStatus, networkType, typeStatus, host, hostStatus, port, portStatus):
		wx.Dialog.__init__(self, None, title=_('Add network connection'), size=(-1,230))
		panel = wx.Panel(self)

		dataLabel = wx.StaticText(panel, label=_('Data'))
		self.data = wx.ComboBox(panel, choices=['NMEA0183', 'SignalK'])
		networkTypeLabel = wx.StaticText(panel, label=_('Type'))
		self.networkType = wx.ComboBox(panel, choices=['TCP', 'UDP'])
		hostLabel = wx.StaticText(panel, label=_('Host'))
		self.host = wx.TextCtrl(panel)
		portLabel = wx.StaticText(panel, label=_('Port'))
		self.port = wx.SpinCtrl(panel, 101, min=4000, max=65536, initial=50000)

		if data: self.data.SetValue(data)
		else: self.data.SetValue('')
		if not dataStatus: self.data.Disable()

		if networkType: self.networkType.SetValue(networkType)
		else: self.networkType.SetValue('')
		if not typeStatus: self.networkType.Disable()

		if host: self.host.SetValue(host)
		else: self.host.SetValue('')
		if not hostStatus: self.host.Disable()

		if port: self.port.SetValue(int(port))
		if not portStatus: self.port.Disable()

		cancelBtn = wx.Button(panel, wx.ID_CANCEL)
		okBtn = wx.Button(panel, wx.ID_OK)

		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox1.Add(dataLabel, 0, wx.LEFT | wx.EXPAND, 10)
		hbox1.Add(self.data, 1, wx.RIGHT | wx.LEFT | wx.EXPAND, 10)

		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		hbox2.Add(networkTypeLabel, 0, wx.LEFT | wx.EXPAND, 10)
		hbox2.Add(self.networkType, 1, wx.RIGHT | wx.LEFT | wx.EXPAND, 10)

		hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		hbox3.Add(hostLabel, 0, wx.LEFT | wx.EXPAND, 10)
		hbox3.Add(self.host, 1, wx.RIGHT | wx.LEFT | wx.EXPAND, 10)

		hbox4 = wx.BoxSizer(wx.HORIZONTAL)
		hbox4.Add(portLabel, 0, wx.LEFT | wx.EXPAND, 10)
		hbox4.Add(self.port, 1, wx.RIGHT | wx.LEFT | wx.EXPAND, 10)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(cancelBtn, 1, wx.ALL | wx.EXPAND, 10)
		hbox.Add(okBtn, 1, wx.ALL | wx.EXPAND, 10)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(hbox1 0, wx.ALL | wx.EXPAND, 5)
		vbox.Add(hbox2 0, wx.ALL | wx.EXPAND, 5)
		vbox.Add(hbox3 0, wx.ALL | wx.EXPAND, 5)
		vbox.Add(hbox4 0, wx.ALL | wx.EXPAND, 5)
		vbox.AddStretchSpacer(1)
		vbox.Add(hbox, 0, wx.EXPAND, 0)

		panel.SetSizer(vbox)
		self.Centre() 
'''

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

import importlib
from .conf import Conf
from .appsList import AppsList

class SerialPorts:
	def __init__(self):
		self.conf = Conf()
		self.currentLanguage = self.conf.get('GENERAL', 'lang')
		if self.conf.get('GENERAL', 'debug') == 'yes': self.debug = True
		else: self.debug = False
		
	def getSerialUsedPorts(self):
		usedPorts=[]
		appsList = AppsList()
		appsDict = appsList.appsDict
		for i in appsDict:
			name = i['module']
			if name:
				serialPorts = False
				try:
					serialPorts = importlib.import_module(name+'.serialPorts')
					if serialPorts: 
						target = serialPorts.SerialPorts(self.conf)
						targetPorts = target.usedSerialPorts()
						if targetPorts:
							for i in targetPorts:
								usedPorts.append(i)
				except Exception as e: 
					if self.debug: print(str(e))
		return usedPorts

	def conflicts(self):
		usedSerialPorts = self.getSerialUsedPorts()
		data = self.conf.get('UDEV', 'Serialinst')
		try: serialinst = eval(data)
		except: serialinst = {}
		def physicalDevice(device):
			alias = device.replace('/dev/', '', 1)
			if alias in serialinst:
				return '/dev/' + serialinst[alias]['device']
			return device
		conflict = []
		for index, connection in enumerate(usedSerialPorts):
			device = physicalDevice(connection['device'])
			if any(index != otherIndex and device == physicalDevice(other['device'])
			       for otherIndex, other in enumerate(usedSerialPorts)):
				result = connection['app']+' -> '+_('connection ID: ')+connection['id']+' | '+_('device: ')+connection['device']
				if result not in conflict: conflict.append(result)
		return conflict if conflict else False

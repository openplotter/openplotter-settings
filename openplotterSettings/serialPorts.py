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

from .conf import Conf

class SerialPorts:
	def __init__(self):
		self.conf = Conf()
		self.currentLanguage = self.conf.get('GENERAL', 'lang')

	def getSerialUsedPorts(self):
		usedPorts=[]

		serialPorts = False
		try:
			from openplotterSignalkInstaller import serialPorts
		except:pass
		if serialPorts: 
			target = serialPorts.SerialPorts(self.conf)
			targetPorts = target.usedSerialPorts()
			if targetPorts:
				for i in targetPorts:
					usedPorts.append(i)

		serialPorts = False
		try:
			from openplotterCan import serialPorts
		except:pass
		if serialPorts: 
			target = serialPorts.SerialPorts(self.conf)
			targetPorts = target.usedSerialPorts()
			if targetPorts:
				for i in targetPorts:
					usedPorts.append(i)

		serialPorts = False
		try:
			from openplotterSerial import serialPorts
		except:pass
		if serialPorts: 
			target = serialPorts.SerialPorts(self.conf)
			targetPorts = target.usedSerialPorts()
			if targetPorts:
				for i in targetPorts:
					usedPorts.append(i)

		serialPorts = False
		try:
			from openplotterOpencpnInstaller import serialPorts
		except:pass
		if serialPorts: 
			target = serialPorts.SerialPorts(self.conf)
			targetPorts = target.usedSerialPorts()
			if targetPorts:
				for i in targetPorts:
					usedPorts.append(i)
					
		return usedPorts


	def conflicts(self):
		usedSerialPorts = self.getSerialUsedPorts()
		data = self.conf.get('UDEV', 'Serialinst')
		try:serialinst = eval(data)
		except:serialinst = {}
		conflict = []
		if usedSerialPorts:
			c = 0
			for i in usedSerialPorts:
				alias = ''
				device = ''
				if 'ttyOP_' in i['device']: alias = i['device']
				else: device = i['device']
				if alias:
					alias2 = alias.replace('/dev/','')
					if alias2 in serialinst:
						device = '/dev/'+serialinst[alias2]['device']
				if device:
					device2 = device.replace('/dev/','')
					for ii in serialinst:
						if serialinst[ii]['device'] == device2: alias = '/dev/'+ii
				c2 = 0
				for iii in usedSerialPorts:
					if alias == iii['device'] or device == iii['device']:
						if c != c2:
							result = i['app']+' -> '+_('connection ID: ')+i['id']+' | '+_('device: ')+i['device']
							if not result in conflict: conflict.append(result)
					c2 = c2 + 1
				c = c + 1
		if conflict: return conflict
		else: return False

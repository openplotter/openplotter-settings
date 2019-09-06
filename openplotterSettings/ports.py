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
from .conf import Conf

class Ports:
	def __init__(self):
		self.conf = Conf()
		self.currentLanguage = self.conf.get('GENERAL', 'lang')

	def getUsedPorts(self):
		usedPorts=[]
		
		ports = False
		try:
			from openplotterI2c import ports
		except:pass
		if ports: 
			target = ports.Ports(self.conf,self.currentLanguage)
			targetPorts = target.usedPorts()
			if targetPorts:
				for i in targetPorts:
					usedPorts.append(i)

		ports = False
		try:
			from openplotterSignalkInstaller import ports
		except:pass
		if ports: 
			target = ports.Ports(self.conf,self.currentLanguage)
			targetPorts = target.usedPorts()
			if targetPorts:
				for i in targetPorts:
					usedPorts.append(i)
		'''	
		ports = False
		try:
			from openplotterOpencpnInstaller import ports
		except:pass
		if ports: 
			target = ports.Ports(self.conf,self.currentLanguage)
			targetPorts = target.usedPorts()
			if targetPorts:
				for i in targetPorts:
					usedPorts.append(i)
		'''
		ports = False
		try:
			from openplotterNetwork import ports
		except:pass
		if ports: 
			target = ports.Ports(self.conf,self.currentLanguage)
			targetPorts = target.usedPorts()
			if targetPorts:
				for i in targetPorts:
					usedPorts.append(i)

		ports = False
		try:
			from openplotterMyapp import ports
		except:pass
		if ports: 
			target = ports.Ports(self.conf,self.currentLanguage)
			targetPorts = target.usedPorts()
			if targetPorts:
				for i in targetPorts:
					usedPorts.append(i)
				
		return usedPorts

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
import subprocess, ujson

class Platform:
	def __init__(self):
		self.isRPI = False
		self.skPort = False
		self.skDir = False
		self.http = 'http://'
		self.admin = 'pkexec'
		
		try:
			modelfile = open('/sys/firmware/devicetree/base/model', 'r', 2000)
			rpimodel = modelfile.read()
			modelfile.close()
			if 'Raspberry' in rpimodel: 
				self.isRPI = True
				self.admin = 'sudo'
		except: pass

		try: 
			service = '/etc/systemd/system/signalk.service'
			with open(service) as data:
				for line in data:
					if 'Environment=EXTERNALPORT=' in line:
						lineList = line.split('=')
						self.skPort = lineList[2].rstrip()
						if self.skPort == '3443': self.http = 'https://'
					if 'WorkingDirectory=' in line:
						lineList = line.split('=')
						self.skDir = lineList[1].rstrip()
		except: pass

	def isInstalled(self,package):
		installed = False
		command = 'LC_ALL=C apt-cache policy '+package
		popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
		for line in popen.stdout:
			if 'Installed:' in line:
				if not '(none)' in line: installed = True
		return installed

	def isSKpluginInstalled(self,plugin):
		installed = False
		data = ''
		file = self.skDir+'/package.json'
		try:
			with open(file) as data_file:
				data = ujson.load(data_file)
				if plugin in data['dependencies']: installed = True
		except: pass
		return installed

	def isSKpluginEnabled(self,plugin):
		Enabled = False
		try:
			setting_file = self.skDir+'/plugin-config-data/'+plugin+'.json'
			data = ''
			with open(setting_file) as data_file:
				data = ujson.load(data_file)
			Enabled = data['enabled']
		except:pass
		return Enabled
			
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
import subprocess, ujson, csv
from .conf import Conf

class Platform:
	def __init__(self):
		self.isRPI = False
		self.skPort = False
		self.skDir = False
		self.http = 'http://'
		self.ws = 'ws://'
		self.admin = 'pkexec'
		self.conf = Conf()
		self.RELEASE_DATA = {}

		if self.conf.get('GENERAL', 'debug') == 'yes': self.debug = True
		else: self.debug = False

		with open("/etc/os-release") as f:
			reader = csv.reader(f, delimiter="=")
			for row in reader:
				if row: self.RELEASE_DATA[row[0]] = row[1]
				
		try: 
			subprocess.check_output(['sudo', '-n', 'echo', 'x'])
			self.admin = 'sudo'
		except: self.admin = 'pkexec'

		try:
			modelfile = open('/sys/firmware/devicetree/base/model', 'r', 2000)
			rpimodel = modelfile.read()
			modelfile.close()
			if 'Raspberry' in rpimodel: self.isRPI = True
		except Exception as e: 
			if self.debug: print('Error getting raspberry model: '+str(e))

		try: 
			service = '/etc/systemd/system/signalk.service'
			with open(service) as data:
				for line in data:
					if 'Environment=EXTERNALPORT=' in line:
						lineList = line.split('=')
						self.skPort = lineList[2].rstrip()
						if self.skPort == '3443' or self.skPort == '443': 
							self.http = 'https://'
							self.ws = 'wss://'
					if 'WorkingDirectory=' in line:
						lineList = line.split('=')
						self.skDir = lineList[1].rstrip()
		except Exception as e: 
			if self.debug: print('Error getting signal k settings: '+str(e))

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
			
	def postInstall(self,version,app):
		currentVersion = self.conf.get('APPS', app)
		if currentVersion: 
			currentVersion = currentVersion.split('.')
			targetVersion = version.split('.')
			if int(currentVersion[0]) < int(targetVersion[0]): return False
			elif int(currentVersion[1]) < int(targetVersion[1]): return False
			elif int(currentVersion[2]) < int(targetVersion[2]): return False
			else: return True
		else: return False

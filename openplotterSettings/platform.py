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
import subprocess

class Platform:
	def __init__(self):
		self.isRPI = False
		self.skPort = False
		self.skDir = False
		
		try:
			modelfile = open('/sys/firmware/devicetree/base/model', 'r', 2000)
			rpimodel = modelfile.read()
			modelfile.close()
			if 'Raspberry' in rpimodel: self.isRPI = True
		except: pass

		try: 
			service = '/etc/systemd/system/signalk.service'
			with open(service) as data:
				for line in data:
					if 'Environment=EXTERNALPORT=' in line:
						lineList = line.split('=')
						self.skPort = lineList[2]
					if 'WorkingDirectory=' in line:
						lineList = line.split('=')
						self.skDir = lineList[1]
		except: pass

	def isInstalled(self,package):
		installed = False
		command = 'LANG=C apt-cache policy '+package
		popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
		for line in popen.stdout:
			if 'Installed:' in line:
				if not '(none)' in line: installed = True
		return installed

			
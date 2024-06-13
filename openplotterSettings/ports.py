#!/usr/bin/env python3

# This file is part of OpenPlotter.
# Copyright (C) 2022 by Sailoog <https://github.com/openplotter/openplotter-settings>>
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

import importlib, sys, subprocess, os
from .conf import Conf
from .appsList import AppsList
from .language import Language

class Ports:
	def __init__(self):
		self.conf = Conf()
		self.currentdir = os.path.dirname(os.path.abspath(__file__))
		self.currentLanguage = self.conf.get('GENERAL', 'lang')
		self.language = Language(self.currentdir,'openplotter-settings',self.currentLanguage)
		if self.conf.get('GENERAL', 'debug') == 'yes': self.debug = True
		else: self.debug = False

	def getUsedPorts(self):
		usedPorts=[]
		try:
			out = subprocess.check_output('raspi-config nonint get_vnc', shell=True).decode(sys.stdin.encoding)
			out = out.replace("'","")
			out = out.strip()
			if out  == '0':
				usedPorts.append({'id':'networkConn1', 'description':_('VNC Remote Desktop'), 'data':[], 'type':'TCP', 'mode':'server', 'address':'localhost', 'port':'5900', 'editable':'0'})
		except: pass
		appsList = AppsList()
		appsDict = appsList.appsDict
		for i in appsDict:
			name = i['module']
			if name:
				ports = False
				try:
					ports = importlib.import_module(name+'.ports')
					if ports: 
						target = ports.Ports(self.conf,self.currentLanguage)
						targetPorts = target.usedPorts()
						if targetPorts:
							for i in targetPorts:
								usedPorts.append(i)
				except Exception as e: 
					if self.debug: print(str(e))
		return usedPorts

	def conflicts(self):
		usedPorts = self.getUsedPorts()
		conflict = []
		if usedPorts:
			for i in usedPorts:
				if i['mode'] == 'server':
					for ii in usedPorts:
						if ii['id'] != i['id'] and ii['mode'] == 'server' and ii['type'] == i['type'] and ii['port'] == i['port']:
							iexists = False
							for iii in conflict:
								if iii['id'] == i['id']: iexists = True
							if not iexists: conflict.append(i)
							iiexists = False
							for iii in conflict:
								if iii['id'] == ii['id']: iiexists = True
							if not iiexists: conflict.append(ii)
		if conflict: return conflict
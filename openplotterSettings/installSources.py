#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2015 by sailoog <https://github.com/sailoog/openplotter>
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

import os, subprocess, sys
from .conf import Conf
from .language import Language
from .platform import Platform

def main():
	try:
		conf2 = Conf()
		platform2 = Platform()
		currentdir = os.path.dirname(os.path.abspath(__file__))
		currentLanguage = conf2.get('GENERAL', 'lang')
		Language(currentdir,'openplotter-settings',currentLanguage)
		beta = conf2.get('GENERAL', 'beta')

		codename_debian = 'buster'
		codename_ubuntu = 'bionic'
		RELEASE_DATA = platform2.RELEASE_DATA
		if RELEASE_DATA['VERSION_CODENAME'] == 'focal': codename_ubuntu = 'focal' #ubuntu
		if RELEASE_DATA['VERSION_CODENAME'] == 'groovy': codename_ubuntu = 'focal' #ubuntu for rasberry
		if RELEASE_DATA['VERSION_CODENAME'] == 'ulyana': codename_ubuntu = 'focal' #mint

		sources = subprocess.check_output('apt-cache policy', shell=True).decode(sys.stdin.encoding)

		fileData = ''
		try:
			fo = open('/etc/apt/sources.list.d/openplotter.list', "r")
			fileData = fo.read()
			fo.close()
		except: pass

		fileDataList = fileData.splitlines()

		deb = 'deb http://ppa.launchpad.net/opencpn/opencpn/ubuntu '+codename_ubuntu+' main'
		if not 'http://ppa.launchpad.net/opencpn/opencpn/ubuntu '+codename_ubuntu in sources:
			if not deb in fileData: fileDataList.append(deb)
			print(_('Added OpenCPN packages source'))
		else: 
			print(_('OpenCPN packages source already exists'))

		deb = 'deb https://www.free-x.de/deb4op '+codename_debian+' main'
		if not 'https://www.free-x.de/deb4op '+codename_debian in sources:
			if not deb in fileData: fileDataList.append(deb)
			print(_('Added XyGrib packages source'))
		else: 
			print(_('XyGrib packages source already exists'))

		deb = 'deb http://ppa.launchpad.net/openplotter/openplotter/ubuntu '+codename_ubuntu+' main'
		if not 'http://ppa.launchpad.net/openplotter/openplotter/ubuntu '+codename_ubuntu in sources:
			if not deb in fileData: fileDataList.append(deb)
			print(_('Added OpenPlotter packages source'))
		else: 
			print(_('OpenPlotter packages source already exists'))

		if beta == 'yes':
			deb = 'deb http://ppa.launchpad.net/sailoog/openplotter/ubuntu '+codename_ubuntu+' main'
			if not 'http://ppa.launchpad.net/sailoog/openplotter/ubuntu '+codename_ubuntu in sources:
				if not deb in fileData: fileDataList.append(deb)
				print(_('Added OpenPlotter beta packages source'))
			else: 
				print(_('OpenPlotter beta packages source already exists'))

		deb = 'deb https://repos.influxdata.com/debian '+codename_debian+' stable'
		if not 'https://repos.influxdata.com/debian '+codename_debian in sources:
			if not deb in fileData: fileDataList.append(deb)
			print(_('Added InfluxDB packages source'))
		else: 
			print(_('InfluxDB packages source already exists'))

		deb = 'deb https://packages.grafana.com/oss/deb stable main'
		if not 'https://packages.grafana.com/oss/deb stable' in sources:
			if not deb in fileData: fileDataList.append(deb)
			print(_('Added Grafana packages source'))
		else: 
			print(_('Grafana packages source already exists'))

		if RELEASE_DATA['ID'] == 'ubuntu': codename_node = codename_ubuntu
		elif RELEASE_DATA['ID'] == 'linuxmint': codename_node = codename_ubuntu
		else: codename_node = codename_debian

		deb = 'deb https://deb.nodesource.com/node_10.x '+codename_node+' main\ndeb-src https://deb.nodesource.com/node_10.x '+codename_node+' main'
		if not 'https://deb.nodesource.com/node_10.x '+codename_node in sources:
			if not deb in fileData: fileDataList.append(deb)
			print(_('Added Node.js 10 packages source'))
		else: 
			print(_('Node.js 10 packages source already exists'))

		removeList = []
		removeList.append('deb https://www.free-x.de/debian buster main contrib non-free')
		removeList.append('deb https://dl.cloudsmith.io/public/openplotter/openplotter/deb/debian buster main')
		removeList.append('deb https://dl.cloudsmith.io/public/openplotter/openplotter-beta/deb/debian buster main')
		if beta != 'yes':
			removeList.append('deb http://ppa.launchpad.net/sailoog/openplotter/ubuntu '+codename_ubuntu+' main')

		finalList = []
		for i in fileDataList:
			if i and not i in removeList: finalList.append(i)

		fileData = '\n'.join(finalList)
		if fileData:
			fo = open('/etc/apt/sources.list.d/openplotter.list', "w")
			fo.write(fileData)
			fo.close()

		os.system('cp -f '+currentdir+'/data/sources/99openplotter /etc/apt/preferences.d')
		os.system('apt-key add - < '+currentdir+'/data/sources/opencpn.gpg.key')
		os.system('apt-key add - < '+currentdir+'/data/sources/oss.boating.gpg.key')
		os.system('apt-key add - < '+currentdir+'/data/sources/openplotter.gpg.key')
		if beta == 'yes': os.system('apt-key add - < '+currentdir+'/data/sources/openplotter.beta.gpg.key')
		os.system('apt-key add - < '+currentdir+'/data/sources/grafana.gpg.key')
		os.system('apt-key add - < '+currentdir+'/data/sources/influxdb.gpg.key')
		os.system('apt-key add - < '+currentdir+'/data/sources/nodesource.gpg.key')

	except Exception as e: print(_('FAILED: ')+str(e))

if __name__ == '__main__':
	main()

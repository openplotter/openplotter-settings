#!/usr/bin/env python3

# This file is part of Openplotter.
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

		codename_debian = 'bookworm'
		conf2.set('GENERAL', 'debianCodeName', codename_debian)
		codename_ubuntu = ['jammy']
		conf2.set('GENERAL', 'ubuntuCodeName', str(codename_ubuntu))

		codeName = ''
		hostID = ''
		RELEASE_DATA = platform2.RELEASE_DATA
		if 'UBUNTU_CODENAME' in RELEASE_DATA: 
			codeName = RELEASE_DATA['UBUNTU_CODENAME']
			hostID = 'ubuntu'
		else: 
			codeName = RELEASE_DATA['VERSION_CODENAME']
			hostID = RELEASE_DATA['ID']
		if hostID != 'ubuntu' and hostID != 'debian':
			print(_('FAILED. Unknown system:')+' '+hostID)
			return
		if hostID == 'debian' and codeName != codename_debian:
			print(_('Current Debian version:')+' '+codeName)
			print(_('FAILED. This version of OpenPlotter only works on this version of Debian:')+' '+codename_debian)
			return
		if hostID == 'ubuntu' and codeName not in codename_ubuntu:
			print(_('Current Ubuntu version:')+' '+codeName)
			print(_('FAILED. This version of OpenPlotter only works on these versions of Ubuntu:')+' '+str(codename_ubuntu))
			return
		conf2.set('GENERAL', 'hostID', hostID)
		conf2.set('GENERAL', 'codeName', codeName)

		sources = subprocess.check_output('apt-cache policy', shell=True).decode(sys.stdin.encoding)

		fileData = ''
		try:
			fo = open('/etc/apt/sources.list.d/openplotter.list', "r")
			fileData = fo.read()
			fo.close()
		except: pass

		fileDataList = fileData.splitlines()

		deb = 'deb https://dl.cloudsmith.io/public/openplotter/openplotter/deb/debian '+codename_debian+' main'
		if not 'https://dl.cloudsmith.io/public/openplotter/openplotter/deb/debian '+codename_debian in sources:
			if not deb in fileData: fileDataList.append(deb)
			print(_('Added OpenPlotter packages source'))
		else: 
			print(_('OpenPlotter packages source already exists'))

		if beta == 'yes':
			deb = 'deb https://dl.cloudsmith.io/public/openplotter/openplotter-beta/deb/debian '+codename_debian+' main'
			if not 'https://dl.cloudsmith.io/public/openplotter/openplotter-beta/deb/debian '+codename_debian in sources:
				if not deb in fileData: fileDataList.append(deb)
				print(_('Added OpenPlotter beta packages source'))
			else: 
				print(_('OpenPlotter beta packages source already exists'))

		deb = 'deb https://www.free-x.de/deb4op '+codename_debian+' main'
		if not 'https://www.free-x.de/deb4op '+codename_debian in sources:
			if not deb in fileData: fileDataList.append(deb)
			print(_('Added free-x packages source'))
		else: 
			print(_('free-x packages source already exists'))

		removeList = []
		if beta != 'yes':
			removeList.append('deb https://dl.cloudsmith.io/public/openplotter/openplotter-beta/deb/debian '+codename_debian+' main')

		finalList = []
		for i in fileDataList:
			if i and not i in removeList: finalList.append(i)

		fileData = '\n'.join(finalList)
		if fileData:
			fo = open('/etc/apt/sources.list.d/openplotter.list', "w")
			fo.write(fileData)
			fo.close()

		os.system('cat '+currentdir+'/data/sources/oss.boating.gpg.key | gpg --dearmor > "/etc/apt/trusted.gpg.d/oss.boating.gpg"')
		os.system('cat '+currentdir+'/data/sources/openplotter.gpg.key | gpg --dearmor > "/etc/apt/trusted.gpg.d/openplotter.gpg"')

		if beta == 'yes': os.system('cat '+currentdir+'/data/sources/openplotter.beta.gpg.key | gpg --dearmor > "/etc/apt/trusted.gpg.d/openplotter.beta.gpg"')

	except Exception as e: print(_('FAILED: ')+str(e))

if __name__ == '__main__':
	main()

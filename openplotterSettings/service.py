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

import sys, os

def shutdown(overlay):
	try:
		config = '/boot/config.txt'
		os.system('cp -f '+config+' '+config+'_back')
		file = open(config, 'r')
	except:
		try:
			config = '/boot/firmware/config.txt'
			os.system('cp -f '+config+' '+config+'_back')
			file = open(config, 'r')
		except Exception as e:
			print(str(e))
			return
	exists = False
	out = ''
	while True:
		line = file.readline()
		if not line: break
		if overlay and 'dtoverlay=gpio-shutdown' in line: 
			out += overlay+'\n'
			exists = True
		elif not overlay and 'dtoverlay=gpio-shutdown' in line: pass
		else: out += line
	if overlay and not exists: out += overlay+'\n'
	file.close()
	try: 
		file = open(config, 'w')
		file.write(out)
		file.close()
	except Exception as e:
		os.system('cp -f '+config+'_back '+config)
		print(str(e))
		return

def poweroff(overlay):
	try:
		config = '/boot/config.txt'
		os.system('cp -f '+config+' '+config+'_back')
		file = open(config, 'r')
	except:
		try:
			config = '/boot/firmware/config.txt'
			os.system('cp -f '+config+' '+config+'_back')
			file = open(config, 'r')
		except Exception as e:
			print(str(e))
			return
	exists = False
	out = ''
	while True:
		line = file.readline()
		if not line: break
		if overlay and 'dtoverlay=gpio-poweroff' in line: 
			out += overlay+'\n'
			exists = True
		elif not overlay and 'dtoverlay=gpio-poweroff' in line: pass
		else: out += line
	if overlay and not exists: out += overlay+'\n'
	file.close()
	try: 
		file = open(config, 'w')
		file.write(out)
		file.close()
	except Exception as e:
		os.system('cp -f '+config+'_back '+config)
		print(str(e))
		return

if sys.argv[1] == 'shutdown': shutdown(sys.argv[2])
if sys.argv[1] == 'poweroff': poweroff(sys.argv[2])
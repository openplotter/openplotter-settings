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

import sys, os, subprocess

def touch(state):
	try:
		config = '/etc/environment'
		os.system('cp -f '+config+' '+config+'_back')
		file = open(config, 'r')
	except Exception as e: print(str(e))
	exists = False
	out = ''
	while True:
		line = file.readline()
		if not line: break
		if state and 'GTK_OVERLAY_SCROLLING=0' in line: 
			out += 'GTK_OVERLAY_SCROLLING=0\n'
			exists = True
		elif not state and 'GTK_OVERLAY_SCROLLING=0' in line: pass
		else: out += line
	if state and not exists: out += 'GTK_OVERLAY_SCROLLING=0\n'
	file.close()
	try: 
		file = open(config, 'w')
		file.write(out)
		file.close()
	except Exception as e:
		os.system('cp -f '+config+'_back '+config)
		print(str(e))

	out = subprocess.check_output('gsettings get org.gnome.desktop.interface gtk-theme', shell=True).decode(sys.stdin.encoding)
	out = out.replace("'","")
	out = out.strip()
	path = '/usr/share/themes/'+out
	if os.path.exists(path):
		css = path+'/gtk-3.0/gtk.css'
		if not os.path.exists(path+'/gtk-3.0'): os.mkdir(path+'/gtk-3.0')
		if not os.path.exists(css):
			file = open(path+'/gtk-3.0/gtk.css', 'w')
			file.write('')
			file.close()

		os.system('cp -f '+css+' '+css+'_back')
		file = open(css, 'r')
		exists = False
		out = ''
		while True:
			line = file.readline()
			if not line: break
			if '@import url("openplotter.css");' in line:
				exists = True
				if state: out += line
				else: pass
			else: out += line
		if state and not exists: out += '@import url("openplotter.css");\n'
		file.close()
		try: 
			file = open(css, 'w')
			file.write(out)
			file.close()
		except Exception as e:
			os.system('cp -f '+css+'_back '+css)
			print('Error setting gtk css: '+str(e))

		try:
			opcss = path+'/gtk-3.0/openplotter.css'
			file = open(opcss, 'w')
			file.write('scrollbar slider { min-width: 20px;min-height: 20px;border-radius: 22px;border: 5px solid transparent; }')
			file.close()
		except Exception as e: print('Error setting gtk css: '+str(e))


def shutdown(overlay):
	try:
		config = '/boot/firmware/config.txt'
		os.system('cp -f '+config+' '+config+'_back')
		file = open(config, 'r')
	except:
		try:
			config = '/boot/config.txt'
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
	if overlay:
		fo = open('/etc/systemd/system/openplotter-shutdown.service', "w")
		fo.write( '[Service]\nEnvironment=OPrescue=0\nEnvironmentFile=/boot/firmware/config.txt\nExecStart=systemd-inhibit --what=shutdown --mode=delay openplotter-shutdown $OPrescue\nUser=root\nRestart=always\nRestartSec=3\n\n[Install]\nWantedBy=local-fs.target')
		fo.close()
		subprocess.call(['systemctl', 'daemon-reload'])
		subprocess.call(['systemctl', 'enable', 'openplotter-shutdown.service'])
	else:
		subprocess.call(['systemctl', 'disable', 'openplotter-shutdown.service'])
		os.system('rm -f /etc/systemd/system/openplotter-shutdown.service')
		subprocess.call(['systemctl', 'daemon-reload'])

def poweroff(overlay):
	try:
		config = '/boot/firmware/config.txt'
		os.system('cp -f '+config+' '+config+'_back')
		file = open(config, 'r')
	except:
		try:
			config = '/boot/config.txt'
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
if sys.argv[1] == 'touch': touch(sys.argv[2])
#!/usr/bin/env python3

# This file is part of OpenPlotter.
# Copyright (C) 2023 by Sailoog <https://github.com/openplotter/openplotter-settings>
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

import subprocess, os, sys

subprocess.call(['raspi-config', 'nonint', 'do_wayland', sys.argv[1]])

if sys.argv[1] == 'W2': 
	command = 'toggle-wvkbd'
	try: subprocess.call(['apt', 'install', '-y', 'wvkbd'])
	except: pass
if sys.argv[1] == 'W1': command = 'toggle-matchbox'

shortcut = '/usr/share/applications/inputmethods/matchbox-keyboard.desktop'
if os.path.exists(shortcut):
	file = open(shortcut, 'r')
	file2 = ''
	while True:
		line = file.readline()
		if not line: break
		if 'Exec=' in line: file2 += 'Exec='+command+'\n'
		else: file2 += line
	file.close()
	file1 = open(shortcut, 'w')
	file1.write(file2)
	file1.close()
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

import os, sys

if sys.argv[1] == 'install':
	os.system('pip3 install rpi_backlight -U')

	udevFile = '/etc/udev/rules.d/backlight-permissions.rules'
	if not os.path.exists(udevFile):
		fo = open(udevFile, "w")
		fo.write( 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"')
		fo.close()
	os.system('udevadm control --reload-rules && udevadm trigger')

	currentdir = os.path.dirname(os.path.abspath(__file__))
	source = currentdir+'/data/openplotter-brightness.desktop'
	os.system('cp -f '+source+' /usr/share/applications')

if sys.argv[1] == 'uninstall':
	os.system('rpi-backlight -b 100')
	os.system('pip3 uninstall -y rpi_backlight')
	os.system('rm -f /etc/udev/rules.d/backlight-permissions.rules')
	os.system('udevadm control --reload-rules && udevadm trigger')
	os.system('rm -f /usr/share/applications/openplotter-brightness.desktop')



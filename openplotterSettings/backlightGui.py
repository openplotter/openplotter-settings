#!/usr/bin/env python3

# This file is part of OpenPlotter.
# Copyright (C) 2024 by Sailoog <https://github.com/openplotter/openplotter-settings>
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

import os, subprocess

def main():
	subprocess.call(['pkill', '-f', 'rpi-backlight-gui'])
	backlightPath = "/sys/class/backlight"
	backlightDevices = os.listdir(backlightPath)
	if backlightDevices: 
		backlightDevice = backlightPath+'/'+backlightDevices[0]
		subprocess.Popen(['rpi-backlight-gui', backlightDevice])

if __name__ == '__main__':
	main()
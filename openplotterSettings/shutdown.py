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

import time, subprocess, sys

def main():
	if sys.argv[1] != '1':
		try:
			config = '/boot/firmware/config.txt'
			file = open(config, 'r')
		except:
			try:
				config = '/boot/config.txt'
				file = open(config, 'r')
			except Exception as e:
				print(str(e))
				return
		gpio = ''
		while True:
			line = file.readline()
			if not line: break
			if 'gpio-shutdown' in line and not '#' in line:
				items = line.split(',')
				for i in items:
					if 'gpio_pin' in i:
						items2 = i.split('=')
						gpio = items2[1]
						gpio = gpio.strip()
		file.close()
		if gpio:
			while True:
				out = subprocess.check_output('pinctrl get '+gpio, shell=True).decode(sys.stdin.encoding)
				out = out.split('|')
				out = out[1].split('//')
				if 'lo' in out[0]:
					subprocess.call('pkill -15 opencpn', shell=True)
					time.sleep(2)
					subprocess.call('halt', shell=True)
				time.sleep(3)


if __name__ == '__main__':
	main()
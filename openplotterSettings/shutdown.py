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
from .conf import Conf

def main():
	conf2 = Conf()
	try: shutdown = eval(conf2.get('GENERAL', 'shutdown'))
	except: shutdown = {}
	if shutdown:
		if shutdown['gpio']:
				while True:
					out = subprocess.check_output('pinctrl get '+shutdown['gpio'], shell=True).decode(sys.stdin.encoding)
					out = out.split('|')
					out = out[1].split('//')
					if 'lo' in out[0]: subprocess.call('poweroff', shell=True)
					time.sleep(1)

if __name__ == '__main__':
	main()
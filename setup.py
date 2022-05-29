#!/usr/bin/env python3

# This file is part of OpenPlotter.
# Copyright (C) 2022 by sailoog <https://github.com/openplotter/openplotter-settings>
#                     e-sailing <https://github.com/e-sailing/openplotter>
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

from setuptools import setup
from openplotterSettings import version

setup (
	name = 'openplotterSettings',
	version = version.version,
	description = 'Main openplotter app',
	license = 'GPLv3',
	author="Sailoog",
	author_email='info@sailoog.com',
	url='https://github.com/openplotter/openplotter-settings',
        install_requires=['wxPython','pyudev','ujson'],
	packages=['openplotterSettings'],
	classifiers = ['Natural Language :: English',
	'Operating System :: POSIX :: Linux',
	'Programming Language :: Python :: 3'],
	include_package_data=True,
	entry_points={'console_scripts': ['openplotter-settings=openplotterSettings.openplotterSettings:main','openplotter-startup=openplotterSettings.startup:main','openplotterPostInstall=openplotterSettings.postInstall:main','settingsPreUninstall=openplotterSettings.settingsPreUninstall:main','settingsSourcesInstall=openplotterSettings.installSources:main']},
	data_files=[('share/applications', ['openplotterSettings/data/openplotter-settings.desktop','openplotterSettings/data/openplotter-check.desktop']),('share/pixmaps', ['openplotterSettings/data/openplotter-settings.png', 'openplotterSettings/data/openplotter-48.png', 'openplotterSettings/data/openplotter-check.png']),
	('share/sounds/openplotter', ['openplotterSettings/data/sounds/Bleep.mp3',
									'openplotterSettings/data/sounds/House_Fire_Alarm.mp3',
									'openplotterSettings/data/sounds/Ship_Bell.mp3',
									'openplotterSettings/data/sounds/Store_Door_Chime.mp3',
									'openplotterSettings/data/sounds/Tornado_Siren_II.mp3',]),
	('share/matchbox-keyboard', ['openplotterSettings/data/keyboards/base-fragment-CAT.xml',
									'openplotterSettings/data/keyboards/keyboard-CAT.xml',
									'openplotterSettings/data/keyboards/arrow2.png',
									'openplotterSettings/data/keyboards/return2.png',
									'openplotterSettings/data/keyboards/shift2.png',
									'openplotterSettings/data/keyboards/shift_caps2.png'])
	]
	)

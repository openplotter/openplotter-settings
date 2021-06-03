#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2019 by Sailoog <https://github.com/openplotter/openplotter-settings>
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

import os
from .conf import Conf
from .platform import Platform

class AppsList:
	def __init__(self):
		conf2 = Conf()
		platform2 = Platform()
		currentdir = os.path.dirname(os.path.abspath(__file__))
		self.appsDict = []

		try: externalApps = eval(conf2.get('APPS', 'external_apps'))
		except Exception as e: 
			print ("wrong external apps format: "+str(e))
			externalApps = []
		for app in externalApps:
			try: self.appsDict.append(app)
			except Exception as e: print ("wrong external app format: "+str(e))

		app = {
		'name': 'SDR VHF',
		'platform': 'both',
		'package': 'openplotter-sdr-vhf',
		'preUninstall': platform2.admin+' sdrVhfPreUninstall',
		'uninstall': 'openplotter-sdr-vhf',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-sdr-vhf',
		'postInstall': platform2.admin+' sdrVhfPostInstall',
		'reboot': 'no',
		'module': 'openplotterSdrVhf',
		'conf': 'sdr_vhf'
		}
		self.appsDict.append(app)

		app = {
		'name': 'Kplex',
		'platform': 'both',
		'package': 'openplotter-kplex',
		'preUninstall': platform2.admin+' kplexPreUninstall',
		'uninstall': 'openplotter-kplex',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-kplex',
		'postInstall': platform2.admin+' kplexPostInstall',
		'reboot': 'no',
		'module': 'openplotterKplex',
		'conf': 'kplex'
		}
		self.appsDict.append(app)

		app = {
		'name': _('Signal K Filter'),
		'platform': 'both',
		'package': 'openplotter-skfilter',
		'preUninstall': platform2.admin+' SKfilterPreUninstall',
		'uninstall': 'openplotter-skfilter',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-SKfilter',
		'postInstall': platform2.admin+' SKfilterPostInstall',
		'reboot': 'no',
		'module': 'openplotterSKfilter',
		'conf': 'SKfilter'
		}
		self.appsDict.append(app)

		app = {
		'name': 'IoT',
		'platform': 'both',
		'package': 'openplotter-iot',
		'preUninstall': platform2.admin+' iotPreUninstall',
		'uninstall': 'openplotter-iot',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-iot',
		'postInstall': platform2.admin+' iotPostInstall',
		'reboot': 'no',
		'module': 'openplotterIot',
		'conf': 'iot'
		}
		self.appsDict.append(app)

		app = {
		'name': _('Notifications'),
		'platform': 'both',
		'package': 'openplotter-notifications',
		'preUninstall': 'iotPreUninstall',
		'uninstall': 'openplotter-notifications',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-notifications',
		'postInstall': platform2.admin+' notificationsPostInstall',
		'reboot': 'no',
		'module': 'openplotterNotifications',
		'conf': 'notifications'
		}
		self.appsDict.append(app)

		app = {
		'name': 'GPIO',
		'platform': 'rpi',
		'package': 'openplotter-gpio',
		'preUninstall': platform2.admin+' gpioPreUninstall',
		'uninstall': 'openplotter-gpio',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-gpio',
		'postInstall': platform2.admin+' gpioPostInstall',
		'reboot': 'no',
		'module': 'openplotterGpio',
		'conf': 'gpio'
		}
		self.appsDict.append(app)

		app = {
		'name': _('I2C Sensors'),
		'platform': 'rpi',
		'package': 'openplotter-i2c',
		'preUninstall': platform2.admin+' i2cPreUninstall',
		'uninstall': 'openplotter-i2c',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-i2c',
		'postInstall': platform2.admin+' i2cPostInstall',
		'reboot': 'no',
		'module': 'openplotterI2c',
		'conf': 'i2c'
		}
		self.appsDict.append(app)

		app = {
		'name': 'Moitessier HAT',
		'platform': 'rpi',
		'package': 'openplotter-moitessier',
		'preUninstall': platform2.admin+' moitessierPreUninstall',
		'uninstall': 'openplotter-moitessier',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-moitessier',
		'postInstall': platform2.admin+' moitessierPostInstall',
		'reboot': 'no',
		'module': 'openplotterMoitessier',
		'conf': 'moitessier'
		}
		self.appsDict.append(app)

		app = {
		'name': 'Pypilot',
		'platform': 'rpi',
		'package': 'openplotter-pypilot',
		'preUninstall': platform2.admin+' pypilotPreUninstall',
		'uninstall': 'openplotter-pypilot',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-pypilot',
		'postInstall': platform2.admin+' pypilotPostInstall',
		'reboot': 'no',
		'module': 'openplotterPypilot',
		'conf': 'pypilot'
		}
		self.appsDict.append(app)

		app = {
		'name': _('CAN Bus'),
		'platform': 'both',
		'package': 'openplotter-can',
		'preUninstall': platform2.admin+' canPreUninstall',
		'uninstall': 'openplotter-can',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-can',
		'postInstall': platform2.admin+' canPostInstall',
		'reboot': 'no',
		'module': 'openplotterCan',
		'conf': 'can'
		}
		self.appsDict.append(app)

		app = {
		'name': _('Serial'),
		'platform': 'both',
		'package': 'openplotter-serial',
		'preUninstall': platform2.admin+' serialPreUninstall',
		'uninstall': 'openplotter-serial',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-serial',
		'postInstall': platform2.admin+' serialPostInstall',
		'reboot': 'no',
		'module': 'openplotterSerial',
		'conf': 'serial'
		}
		self.appsDict.append(app)

		app = {
		'name': _('Network'),
		'platform': 'both',
		'package': 'openplotter-network',
		'preUninstall': platform2.admin+' networkPreUninstall',
		'uninstall': 'openplotter-network',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-network',
		'postInstall': platform2.admin+' networkPostInstall',
		'reboot': 'no',
		'module': 'openplotterNetwork',
		'conf': 'network'
		}
		self.appsDict.append(app)

		app = {
		'name': _('Dashboards'),
		'platform': 'both',
		'package': 'openplotter-dashboards',
		'preUninstall': '',
		'uninstall': 'openplotter-dashboards',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu','https://repos.influxdata.com/debian','https://packages.grafana.com/oss/deb'],
		'dev': 'no',
		'entryPoint': 'openplotter-dashboards',
		'postInstall': '',
		'reboot': 'no',
		'module': 'openplotterDashboards',
		'conf': ''
		}
		self.appsDict.append(app)

		app = {
		'name': 'XyGrib',
		'platform': 'both',
		'package': 'xygrib',
		'preUninstall': '',
		'uninstall': 'xygrib',
		'sources': ['https://www.free-x.de/deb4op'],
		'dev': 'no',
		'entryPoint': 'XyGrib',
		'postInstall': platform2.admin+' python3 '+currentdir+'/xygribPostInstall.py',
		'reboot': 'no',
		'module': '',
		'conf': ''
		}
		self.appsDict.append(app)

		app = {
		'name': _('AvNav Installer'),
		'platform': 'both',
		'package': 'openplotter-avnav',
		'preUninstall': platform2.admin+' avPreUninstall',
		'uninstall': 'openplotter-avnav',
		'sources': ['https://www.free-x.de/deb4op'],
		'dev': 'no',
		'entryPoint': 'openplotter-avnav',
		'postInstall': platform2.admin+' avPostInstall',
		'reboot': 'no',
		'module': 'openplotterAvnav',
		'conf': 'avnav'
		}
		self.appsDict.append(app)
		
		app = {
		'name': _('Signal K Installer'),
		'platform': 'both',
		'package': 'openplotter-signalk-installer',
		'preUninstall': platform2.admin+' signalkPreUninstall',
		'uninstall': 'openplotter-signalk-installer',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu','https://deb.nodesource.com/node_10.x'],
		'dev': 'no',
		'entryPoint': 'openplotter-signalk-installer',
		'postInstall': platform2.admin+' signalkPostInstall',
		'reboot': 'no',
		'module': 'openplotterSignalkInstaller',
		'conf': 'signalk'
		}
		self.appsDict.append(app)
		
		app = {
		'name': _('OpenCPN Installer'),
		'platform': 'both',
		'package': 'openplotter-opencpn-installer',
		'preUninstall': '',
		'uninstall': 'openplotter-opencpn-installer opencpn',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu','http://ppa.launchpad.net/opencpn/opencpn/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-opencpn-installer',
		'postInstall': '',
		'reboot': 'no',
		'module': 'openplotterOpencpnInstaller',
		'conf': ''
		}
		self.appsDict.append(app)

		app = {
		'name': _('Documentation'),
		'platform': 'both',
		'package': 'openplotter-doc',
		'preUninstall': '',
		'uninstall': 'openplotter-doc',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'x-www-browser /usr/share/openplotter-doc/index.html',
		'postInstall': '',
		'reboot': 'no',
		'module': '',
		'conf': ''
		}
		self.appsDict.append(app)

		app = {
		'name': _('Settings'),
		'platform': 'both',
		'package': 'openplotter-settings',
		'preUninstall': platform2.admin+' settingsPreUninstall',
		'uninstall': 'openplotter-settings',
		'sources': ['http://ppa.launchpad.net/openplotter/openplotter/ubuntu'],
		'dev': 'no',
		'entryPoint': 'openplotter-settings',
		'postInstall': '',
		'reboot': 'no',
		'module': '',
		'conf': ''
		}
		self.appsDict.append(app)
		
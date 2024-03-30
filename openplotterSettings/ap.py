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

import sys, subprocess, os, uuid, time

def main():
	if sys.argv[1] == 'enable':

		if not os.path.exists('/etc/NetworkManager/system-connections/OpenPlotter-Hotspot.nmconnection'):
			uuidKey = str(uuid.uuid4())
			timestamp = str(int(time.time()))
			fo = open('/etc/NetworkManager/system-connections/OpenPlotter-Hotspot.nmconnection', "w")
			fo.write( '[connection]\nid=OpenPlotter-Hotspot\nuuid='+uuidKey+'\ntype=wifi\ninterface-name=wlan9\ntimestamp='+timestamp+'\n[wifi]\nmode=ap\nssid=OpenPlotter\n[wifi-security]\nkey-mgmt=wpa-psk\npsk=12345678\n[ipv4]\nmethod=shared\n[ipv6]\naddr-gen-mode=stable-privacy\nmethod=ignore\n[proxy]')
			fo.close()
			subprocess.call(['chmod', '600', '/etc/NetworkManager/system-connections/OpenPlotter-Hotspot.nmconnection'])

		fo = open('/etc/systemd/system/create_ap_interface.service', "w")
		fo.write( '[Unit]\nDescription=Create Virtual WLAN Interface\nWants=network-pre.target\nBefore=network-pre.target\nBindsTo=sys-subsystem-net-devices-wlan0.device\nAfter=sys-subsystem-net-devices-wlan0.device\n[Service]\nType=oneshot\nExecStart=create_ap_interface\n[Install]\nWantedBy=multi-user.target')
		fo.close()

		subprocess.call(['systemctl', 'enable', 'create_ap_interface.service'])

	elif sys.argv[1] == 'disable':

		subprocess.call(['systemctl', 'disable', 'create_ap_interface.service'])

if __name__ == '__main__':
	main()
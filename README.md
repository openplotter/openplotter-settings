## openplotter-settings

Main OpenPlotter app

### Installing

Install dependencies (for production and development):

`sudo apt install python-configparser python3-wxgtk4.0 whois`

#### For production

Download the latest .deb file from [releases](https://github.com/openplotter/openplotter-settings/releases) and install it:

`sudo dpkg -i openplotter-settings_x.x.x-xxx.deb`

#### For development

Clone the repository:

`git clone https://github.com/openplotter/openplotter-settings.git`

Make your changes and test them:

`sudo python3 setup.py install`

Pull request your changes to github and we will check and add them to the next version of the [Debian package](https://launchpad.net/~openplotter/+archive/ubuntu/openplotter/).

### Documentation

https://openplotter.readthedocs.io

### Support

http://forum.openmarine.net/forumdisplay.php?fid=1
import os

def main():
	currentdir = os.path.dirname(__file__)
	source = currentdir+'/data/xygrib.desktop'
	os.system('cp -f '+source+' /usr/share/applications')

if __name__ == '__main__':
	main()

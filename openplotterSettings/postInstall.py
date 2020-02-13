import wx, os, subprocess, sys, time
import wx.richtext as rt
from .conf import Conf
from .language import Language

class MyFrame(wx.Frame):
	def __init__(self, command):
		self.command = command
		conf2 = Conf()
		currentdir = os.path.dirname(os.path.abspath(__file__))
		currentLanguage = conf2.get('GENERAL', 'lang')
		Language(currentdir,'openplotter-settings',currentLanguage)

		wx.Frame.__init__(self, None, title=_('Post-installation actions'), size=(600,300))
		self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		icon = wx.Icon(currentdir+"/data/openplotter-48.png", wx.BITMAP_TYPE_PNG)
		self.SetIcon(icon)
		self.CreateStatusBar()
		font_statusBar = self.GetStatusBar().GetFont()
		font_statusBar.SetWeight(wx.BOLD)
		self.GetStatusBar().SetFont(font_statusBar)
		panel = wx.Panel(self, wx.ID_ANY)



		self.logger = rt.RichTextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_DONTWRAP|wx.LC_SORT_ASCENDING)
		self.logger.SetMargins((10,10))

		self.okButton =wx.Button(panel, label=_('Start'))
		self.okButton.Bind(wx.EVT_BUTTON, self.OnOkButton)
		self.cancelButton =wx.Button(panel, label=_('Cancel'))
		self.cancelButton.Bind(wx.EVT_BUTTON, self.OnCloseButton)
		self.closeButton =wx.Button(panel, label=_('Close'))
		self.closeButton.Bind(wx.EVT_BUTTON, self.OnCloseButton)

		buttons = wx.BoxSizer(wx.VERTICAL)
		buttons.Add(self.okButton, 0, wx.ALL | wx.EXPAND, 5)
		buttons.Add(self.cancelButton, 0, wx.ALL | wx.EXPAND, 5)
		buttons.Add(self.closeButton, 0, wx.ALL | wx.EXPAND, 5)

		main = wx.BoxSizer(wx.HORIZONTAL)
		main.Add(self.logger, 1, wx.ALL | wx.EXPAND, 5)
		main.Add(buttons, 0, wx.ALL | wx.EXPAND, 5)

		panel.SetSizer(main)
		self.Centre()

		self.closeButton.Disable()
		self.logger.WriteText(_('This application has been updated recently and it needs to configure your system to work properly. Please be patient, it could take some time.'))
		self.logger.Newline()
		self.logger.Newline()
		self.logger.WriteText(_('Press Start.'))

	def ShowStatusBar(self, w_msg, colour):
		self.GetStatusBar().SetForegroundColour(colour)
		self.SetStatusText(w_msg)

	def ShowStatusBarYELLOW(self, w_msg):
		self.ShowStatusBar(w_msg,(255,140,0))

	def ShowStatusBarGREEN(self, w_msg):
		self.ShowStatusBar(w_msg, (0,130,0))

	def OnOkButton(self,e):
		self.ShowStatusBarYELLOW(_('Performing pending actions, please wait... '))
		self.logger.Clear()
		popen = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
		for line in popen.stdout:
			if not 'Warning' in line and not 'WARNING' in line:
				self.logger.WriteText(line)
				self.ShowStatusBarYELLOW(_('Performing pending actions, please wait... ')+line)
				self.logger.ShowPosition(self.logger.GetLastPosition())

		self.ShowStatusBarGREEN(_('Done. Close this window and open the app again.'))
		self.okButton.Disable()
		self.cancelButton.Disable()
		self.closeButton.Enable()

	def OnCloseButton(self,e):
		self.Destroy()

def main():
	app = wx.App()
	MyFrame(sys.argv[1]).Show()
	time.sleep(1)
	app.MainLoop()
	
if __name__ == '__main__':
	main()
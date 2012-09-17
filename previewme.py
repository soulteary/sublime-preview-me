
#	   _____ ____  __  ____  _______________    ______  __
#	  / ___// __ \/ / / / / /_  __/ ____/   |  / __ \ \/ /
#	  \__ \/ / / / / / / /   / / / __/ / /| | / /_/ /\  / 
#	 ___/ / /_/ / /_/ / /___/ / / /___/ ___ |/ _, _/ / /  
#	/____/\____/\____/_____/_/ /_____/_/  |_/_/ |_| /_/   
#	                                                      
#						SOULTEARY.COM
#

import sublime, sublime_plugin
import os, platform, tempfile, webbrowser

__FILE_NAME__		= '';
__SYSTEM_INFO__		= '';


def ConvertString(string):
	string = string.encode('ascii', 'ignore')
	if '"' == string[0:1]:
		string = string[1:-1]
	return string


def GetPlatformInfo():
	thePlat = platform.uname()
	if "Windows" == thePlat[0]:
		if "5" == thePlat[3][0:1]:
			return 'WINXP'
		elif "6" == thePlat[3][0:1]:
			return 'WIN7'
	elif "Linux" == thePlat[0]:
		return 'LINUX'
	else:
		return 'OTHER SYSTEM'


def GetPathForChrome():
	global __SYSTEM_INFO__
	import _winreg

	if 'WIN' == __SYSTEM_INFO__[0:3]:
		regPath 	= "Software\\Google\\Update\\ClientState"
		regHandle = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,regPath)
		i = 0
		subKey= _winreg.EnumKey(regHandle, i)
		while subKey:
			queryPath = "Software\\Google\\Update\\ClientState\\" + subKey
			queryReg = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,queryPath)
			appPath, types = _winreg.QueryValueEx(queryReg, "InstallerSuccessLaunchCmdLine")

			if -1 != appPath.find('chrome.exe'):
			 	return appPath
			else:
				i += 1
				subKey= _winreg.EnumKey(regHandle, i)


def GetPathForFireFox():
	global __SYSTEM_INFO__
	import _winreg

	if 'WIN' == __SYSTEM_INFO__[0:3]:
		regPath 	= "Software\\Mozilla\\Mozilla Firefox"
		regHandle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,regPath)
		i = 0
		subKey= _winreg.EnumKey(regHandle, i)
		while subKey:
			queryPath = "Software\\Mozilla\\Mozilla Firefox\\" + subKey + "\\Main"
			queryReg = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,queryPath)
			appPath, type = _winreg.QueryValueEx(queryReg, "PathToExe")
			if -1 != appPath.find('firefox.exe'):
			 	return appPath
			i += 1
			subKey= _winreg.EnumKey(regHandle, i)



def GetPathForSafari():
	global __SYSTEM_INFO__
	import _winreg

	if 'WIN' == __SYSTEM_INFO__[0:3]:
		queryReg = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,"Software\\Apple Computer, Inc.\\Safari")
		appPath, type = _winreg.QueryValueEx(queryReg, "BrowserExe")
		if -1 != appPath.find('Safari.exe'):
		 	return appPath


def GetPathForInternetExplorer():
	global __SYSTEM_INFO__
	import _winreg

	if 'WIN' == __SYSTEM_INFO__[0:3]:
		sysDisk = os.getenv('windir')[0:3]
		if os.path.isfile(sysDisk+'Program Files\\Internet Explorer\\iexplore.exe'):
			return sysDisk+'Program Files\\Internet Explorer\\iexplore.exe'
		else:
			return None


def GetPathForOpera():
	global __SYSTEM_INFO__
	import _winreg

	if 'WIN' == __SYSTEM_INFO__[0:3]:

		queryPath = "Software\\Opera Software"
		queryReg = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,queryPath)
		appPath, type = _winreg.QueryValueEx(queryReg, "Last Install Path")
		appPath += "opera.exe"
	 	return appPath


def OpenBroswer(appName,appPath):
	global __FILE_NAME__
	appName = ConvertString(appName)
	appPath = ConvertString(appPath)
	broswer = webbrowser.BackgroundBrowser(appPath)
	register = webbrowser.register(appName, None, broswer)
	soulteary = webbrowser.get(appName)
	if None != soulteary:
		soulteary.open(__FILE_NAME__)


def CreateHtmlTemplate(strTmp):
	strHTML  = "<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>Page Rreview</title><body>"
	strHTML += strTmp
	strHTML += '</body></html>'
	return strHTML


class PreviewMeCommand(sublime_plugin.TextCommand):

	def run(self, edit, broswer):
		global __SYSTEM_INFO__
		global __FILE_NAME__

		fileName = self.view.file_name()
		if None == fileName:
			tmpFile =  tempfile.NamedTemporaryFile(suffix = ".html", delete = False)
			region = sublime.Region(0, self.view.size())
			text = self.view.substr(region)
			text = text.encode('utf-8')
			tmpFile.write(CreateHtmlTemplate(text))
			tmpFile.close()
			__FILE_NAME__ = tmpFile.name
		else:
			__FILE_NAME__ = fileName

		__FILE_NAME__ = __FILE_NAME__.encode('utf-8')
		__SYSTEM_INFO__ = GetPlatformInfo()


		if 'WIN' == __SYSTEM_INFO__[0:3]:
			if 'Chrome' == broswer:
				OpenBroswer(broswer, GetPathForChrome())
			elif 'FireFox' == broswer:
				OpenBroswer(broswer, GetPathForFireFox())
			elif 'Safari' == broswer:
				OpenBroswer(broswer, GetPathForSafari())
			elif 'Internet Explorer' == broswer:
				OpenBroswer(broswer, GetPathForInternetExplorer())
			elif 'Opera' == broswer:
				OpenBroswer(broswer, GetPathForOpera())
			else:
				sublime.status_message('Preview Content By ' + broswer + ' Failure.')
		elif 'LINUX' == __SYSTEM_INFO__:
			if 'Chrome' == broswer:
				os.popen(r"/usr/bin/chromium-browser "+__FILE_NAME__)
			elif 'FireFox' == broswer:
				os.popen(r"firefox "+__FILE_NAME__)
			elif 'Opera' == broswer:
				os.popen(r"/usr/bin/opera "+__FILE_NAME__)
			else:
				sublime.status_message('Preview Content By ' + broswer + ' Failure.')
				return
		else:
			sublime.status_message('Preview Content On ' + __SYSTEM_INFO__ + ' Failure.')
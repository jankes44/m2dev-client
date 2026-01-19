import net
import app
import ui
import uiOption

import uiSystemOption
import uiGameOption
import uiScriptLocale
import networkModule
import constInfo
import localeInfo
import serverInfo
import chat
import ServerStateChecker

SYSTEM_MENU_FOR_PORTAL = False

###################################################################################################
## System
class SystemDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
	
	def __Initialize(self):
		self.eventOpenHelpWindow = None
		self.systemOptionDlg = None
		self.gameOptionDlg = None

		self.moveChannelDialog = None
		
		
	def LoadDialog(self):	
		if SYSTEM_MENU_FOR_PORTAL:
			self.__LoadSystemMenu_ForPortal()
		else:
			self.__LoadSystemMenu_Default()
			
	def __LoadSystemMenu_Default(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/systemdialog.py")

		self.GetChild("system_option_button").SAFE_SetEvent(self.__ClickSystemOptionButton)
		self.GetChild("game_option_button").SAFE_SetEvent(self.__ClickGameOptionButton)
		self.GetChild("change_button").SAFE_SetEvent(self.__ClickChangeCharacterButton)
		self.GetChild("movechannel_button").SAFE_SetEvent(self.__ClickMoveChannelButton)
		self.GetChild("logout_button").SAFE_SetEvent(self.__ClickLogOutButton)
		self.GetChild("exit_button").SAFE_SetEvent(self.__ClickExitButton)
		self.GetChild("help_button").SAFE_SetEvent(self.__ClickHelpButton)
		self.GetChild("cancel_button").SAFE_SetEvent(self.Close)
		self.GetChild("mall_button").SAFE_SetEvent(self.__ClickInGameShopButton)

	def __LoadSystemMenu_ForPortal(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/systemdialog_forportal.py")

		self.GetChild("system_option_button").SAFE_SetEvent(self.__ClickSystemOptionButton)
		self.GetChild("game_option_button").SAFE_SetEvent(self.__ClickGameOptionButton)
		self.GetChild("change_button").SAFE_SetEvent(self.__ClickChangeCharacterButton)
		self.GetChild("exit_button").SAFE_SetEvent(self.__ClickExitButton)
		self.GetChild("help_button").SAFE_SetEvent(self.__ClickHelpButton)
		self.GetChild("cancel_button").SAFE_SetEvent(self.Close)
		

	def Destroy(self):
		self.ClearDictionary()
		
		if self.gameOptionDlg:
			self.gameOptionDlg.Destroy()
			
		if self.systemOptionDlg:
			self.systemOptionDlg.Destroy()

		if self.moveChannelDialog:
			self.moveChannelDialog.Destroy()
			
		self.__Initialize()

	def SetOpenHelpWindowEvent(self, event):
		self.eventOpenHelpWindow = event

	def OpenDialog(self):
		self.Show()

	def __ClickChangeCharacterButton(self):
		self.Close()

		net.ExitGame()

	def __OnClosePopupDialog(self):
		self.popup = None		

	def __ClickLogOutButton(self):
		if SYSTEM_MENU_FOR_PORTAL: 
			if app.loggined:
				self.Close()
				net.ExitApplication()
			else:
				self.Close()
				net.LogOutGame()
		else:
			self.Close()
			net.LogOutGame()

	def __ClickMoveChannelButton(self):
		self.Close()
		
		if not self.moveChannelDialog:
			self.moveChannelDialog = MoveChannelDialog()

		self.moveChannelDialog.Show()

	def __ClickExitButton(self):
		self.Close()
		net.ExitApplication()
		
	def __ClickSystemOptionButton(self):
		self.Close()

		if not self.systemOptionDlg:
			self.systemOptionDlg = uiSystemOption.OptionDialog()

		self.systemOptionDlg.Show()

	def __ClickGameOptionButton(self):
		self.Close()

		if not self.gameOptionDlg:
			self.gameOptionDlg = uiGameOption.OptionDialog()

		self.gameOptionDlg.Show()

	
	def __ClickHelpButton(self):
		self.Close()

		if None != self.eventOpenHelpWindow:
			self.eventOpenHelpWindow()

	def __ClickInGameShopButton(self):
		self.Close()
		net.SendChatPacket("/in_game_mall")

	def Close(self):
		self.Hide()
		return True

	def RefreshMobile(self):
		if self.gameOptionDlg:
			self.gameOptionDlg.RefreshMobile()
		#self.optionDialog.RefreshMobile()

	def OnMobileAuthority(self):
		if self.gameOptionDlg:
			self.gameOptionDlg.OnMobileAuthority()
		#self.optionDialog.OnMobileAuthority()

	def OnBlockMode(self, mode):
		uiGameOption.blockMode = mode
		if self.gameOptionDlg:
			self.gameOptionDlg.OnBlockMode(mode)
		#self.optionDialog.OnBlockMode(mode)

	def OnChangePKMode(self):
		if self.gameOptionDlg:
			self.gameOptionDlg.OnChangePKMode()
		#self.optionDialog.OnChangePKMode()
	
	def OnPressExitKey(self):
		self.Close()
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True

if __name__ == "__main__":

	import app
	import wndMgr
	import systemSetting
	import mouseModule
	import grp
	import ui
	import chr
	import background
	import player

	#wndMgr.SetOutlineFlag(True)

	app.SetMouseHandler(mouseModule.mouseController)
	app.SetHairColorEnable(True)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	app.Create("METIN2 CLOSED BETA", systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	mouseModule.mouseController.Create()


	wnd = SystemDialog()
	wnd.LoadDialog()
	wnd.Show()

	app.Loop()

class MoveChannelDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
	
		self.channelIndex = net.GetServerInfo().strip().split(", ")[1]	
		self.moveChannelIndex = 0
		
		self.channelButtons = []
		self.channelNames = []		
		self.channelStates = []
		
		# Use constInfo values
		self.regionID = constInfo.REGION_ID
		self.serverID = constInfo.SERVER_ID
		
		self.channelDict = serverInfo.REGION_DICT[self.regionID][self.serverID]["channel"]		
		
		self.__LoadWindow()
		self.Open()		
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print " -------------------------------------- DELETE MOVE CHANNEL DIALOG"
		
	def Destroy(self):
		self.Close()
		self.ClearDictionary()
		print " -------------------------------------- DESTROY MOVE CHANNEL DIALOG"	

	def NotifyChannelState(self, addrKey, state):
		try:
			stateName=serverInfo.STATE_DICT[state]
		except:
			stateName=serverInfo.STATE_NONE

		regionID=int(addrKey/1000)
		serverID=int(addrKey/10) % 100
		channelID=addrKey%10

		try:
			serverInfo.REGION_DICT[regionID][serverID]["channel"][channelID]["state"] = stateName
		except:
			import exception
			exception.Abort(localeInfo.CHANNEL_NOT_FIND_INFO)
		
		
	def RefreshChannelState(self):
		try:
			ServerStateChecker.Create(self)

			for channelID, channelDataDict in self.channelDict.items():
				key=channelDataDict["key"]
				ip=channelDataDict["ip"]
				udp_port=channelDataDict["udp_port"]
				ServerStateChecker.AddChannel(key, ip, udp_port)

			ServerStateChecker.Request()

			for channelID, channelDataDict in self.channelDict.items():
				#self.channelButtons[channelID - 1].SetText("|cFF%s%s" % (serverInfo.STATE_COLOR_DICT[serverInfo.REGION_DICT[self.regionID][self.serverID]["channel"][channelID]["state"]], channelDataDict["name"]))
				self.channelButtons[channelID - 1].SetText(localeInfo.HexColorAnyText(channelDataDict["name"], serverInfo.STATE_COLOR_DICT[serverInfo.REGION_DICT[self.regionID][self.serverID]["channel"][channelID]["state"]]))
		except:
			pass
		
	def OnUpdate(self):
		ServerStateChecker.Update()
		
	def __LoadWindow(self):
		# Create window programmatically instead of loading from script
		self.SetWindowName("MoveChannelDialog")
		self.SetSize(200, 300)  # Will be resized in Open()
		
		self.moveChannelBoard = ui.Board()
		self.moveChannelBoard.SetParent(self)
		self.moveChannelBoard.SetSize(200, 300)  # Will be resized in Open()
		self.moveChannelBoard.SetPosition(0, 0)
		self.moveChannelBoard.Show()
		
		self.titleBar = ui.TitleBar()
		self.titleBar.SetParent(self.moveChannelBoard)
		self.titleBar.MakeTitleBar(190 - 13, "red")
		self.titleBar.SetPosition(6, 7)
		self.titleBar.Show()
		
		self.titleName = ui.TextLine()
		self.titleName.SetParent(self.titleBar)
		self.titleName.SetPosition(0, 4)
		self.titleName.SetWindowHorizontalAlignCenter()
		self.titleName.SetHorizontalAlignCenter()
		self.titleName.SetText(localeInfo.MOVE_CHANNEL_TITLE)
		self.titleName.Show()
		
		self.blackBoard = ui.ThinBoard()
		self.blackBoard.SetParent(self.moveChannelBoard)
		self.blackBoard.SetPosition(13, 36)
		self.blackBoard.SetSize(161, 100)  # Will be resized in Open()
		self.blackBoard.Show()

	def Open(self):
		try:
			# moveChannelBoard and blackBoard already created in __LoadWindow()
			# No need to use GetChild since we created them programmatically
			
			for channelID, channelDataDict in self.channelDict.items():
				btn = ui.Button()
				btn.SetParent(self.blackBoard)
				btn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
				btn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
				btn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
				btn.SetText(channelDataDict["name"])
				btn.SetPosition(40, 6 + (28 * (channelID - 1)))
				btn.SAFE_SetEvent(self.__SelectChannel, channelID - 1)
				btn.Show()
				
				self.channelButtons.append(btn)
				self.channelNames.append(channelDataDict["name"])
				self.channelStates.append(serverInfo.REGION_DICT[self.regionID][self.serverID]["channel"][channelID]["state"])

			if self.channelIndex in self.channelNames:
				self.channelIndex = self.channelNames.index(self.channelIndex)
				self.channelButtons[self.channelIndex].Down()	
				self.channelButtons[self.channelIndex].Disable()				
				
			self.acceptButton = ui.Button()
			self.acceptButton.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
			self.acceptButton.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
			self.acceptButton.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
			self.acceptButton.SetParent(self.moveChannelBoard)
			self.acceptButton.SetPosition(13, 22 + (28 * (len(self.channelButtons) + 1)))
			self.acceptButton.SetText(localeInfo.UI_ACCEPT)
			self.acceptButton.SAFE_SetEvent(self.AcceptButton)
			self.acceptButton.Show()
			
			self.closeButton = ui.Button()
			self.closeButton.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
			self.closeButton.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
			self.closeButton.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
			self.closeButton.SetParent(self.moveChannelBoard)
			self.closeButton.SetPosition(114, 22 + (28 * (len(self.channelButtons) + 1)))
			self.closeButton.SetText(localeInfo.UI_CANCEL)
			self.closeButton.SAFE_SetEvent(self.Close)
			self.closeButton.Show()		
				
			self.SetSize(190, len(self.channelButtons)* 28 + 74 + 9)	
			self.moveChannelBoard.SetSize(190, len(self.channelButtons) * 28 + 74 + 9)	
			self.blackBoard.SetSize(161, len(self.channelButtons) * 28 + 8)				
		except:
			import exception
			exception.Abort("MoveChannelDialog.Open.BindObject")

		ui.ScriptWindow.Show(self)			
			
	def __SelectChannel(self, index):	
		self.channelButtons[self.channelIndex].SetUp()
		self.channelButtons[self.channelIndex].Enable()	
		self.channelIndex = index
		self.channelButtons[self.channelIndex].Down()
		self.channelButtons[self.channelIndex].Disable()
			
	def AcceptButton(self):
		if self.channelNames[self.channelIndex]== net.GetServerInfo().strip().split(", ")[1]:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHANNEL_NOTIFY_SAME)
			return
		elif self.channelStates[self.channelIndex] == serverInfo.STATE_DICT[3]:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHANNEL_NOTIFY_FULL)
			return
		elif self.channelStates[self.channelIndex] == serverInfo.STATE_DICT[0]:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHANNEL_NOTIFY_OFFLINE)
			return

		else:
			self.Close()
			net.SendChatPacket("/move_channel %d" % int(self.channelIndex + 1))	 #your command to change channel
			
	def Close(self):
		#self.__SelectChannel(self.channelNames.index(net.GetServerInfo().strip().split(", ")[1]))
		self.Hide()
		return True
		
	def Show(self):
		ui.ScriptWindow.Show(self)
		self.SetCenterPosition()
		self.RefreshChannelState()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True

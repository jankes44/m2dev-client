import ui
import uiScriptLocale
import net
import app
import localeInfo

# Mob configuration - add icon paths if you find actual icons
MOB_LIST = {
	171: {"name": "Wild Dog", "level": 1, "icon": "icon/item/27001.tga"},  # Placeholder
	173: {"name": "Wolf", "level": 5, "icon": "icon/item/27002.tga"},
	180: {"name": "Bear", "level": 12, "icon": "icon/item/27003.tga"},
	184: {"name": "Tiger", "level": 18, "icon": "icon/item/27004.tga"},
	185: {"name": "White Tiger", "level": 25, "icon": "icon/item/27005.tga"},
}

class IdleHuntingWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		
		# State data
		self.state = 0
		self.mob_vnum = 0
		self.time_left = 0
		self.hunt_duration = 0
		self.max_daily = 28800
		self.total_today = 0
		
		# UI elements
		self.board = None
		self.titleBar = None
		self.progressBar = None
		self.timeText = None
		self.stateText = None
		
		# State 0 - Mob selection
		self.mobButtons = []
		self.startButton = None
		
		# State 1 - Pending
		self.mobImage = None
		self.pendingText = None
		self.cancelButton = None
		
		# State 2 - Claimable
		self.summaryText = None
		self.claimButton = None
		
		self.LoadWindow()
	
	def __del__(self):
		ui.ScriptWindow.__del__(self)
	
	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/idlehuntingwindow.py")
		except:
			import exception
			exception.Abort("IdleHuntingWindow.LoadWindow")
		
		try:
			self.board = self.GetChild("board")
			self.titleBar = self.GetChild("TitleBar")
			self.progressBar = self.GetChild("ProgressBar")
			self.timeText = self.GetChild("TimeText")
			self.stateText = self.GetChild("StateText")
		except:
			import exception
			exception.Abort("IdleHuntingWindow.LoadWindow.BindObject")
		
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		
		# Create mob selection buttons (state 0)
		self.__CreateMobSelectionUI()
		
		# Create pending UI (state 1)
		self.__CreatePendingUI()
		
		# Create claimable UI (state 2)
		self.__CreateClaimableUI()
	
	def __CreateMobSelectionUI(self):
		self.mobButtons = []
		xPos = 20
		yPos = 100
		
		for mob_vnum, mob_data in MOB_LIST.items():
			btn = ui.Button()
			btn.SetParent(self.board)
			btn.SetPosition(xPos, yPos)
			btn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			btn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			btn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			btn.SetText("%s (Lv %d)" % (mob_data["name"], mob_data["level"]))
			btn.SetEvent(ui.__mem_func__(self.OnClickMob), mob_vnum)
			btn.Hide()
			self.mobButtons.append(btn)
			
			xPos += 110
			if len(self.mobButtons) % 3 == 0:
				xPos = 20
				yPos += 40
		
		self.startButton = ui.Button()
		self.startButton.SetParent(self.board)
		self.startButton.SetPosition(0, 0)
		self.startButton.SetText("Start Hunting")
		self.startButton.Hide()
	
	def __CreatePendingUI(self):
		self.pendingText = ui.TextLine()
		self.pendingText.SetParent(self.board)
		self.pendingText.SetFontName("Tahoma:14")
		self.pendingText.SetPosition(0, 140)
		self.pendingText.SetWindowHorizontalAlignCenter()
		self.pendingText.SetHorizontalAlignCenter()
		self.pendingText.SetText("Log out to start hunting!")
		self.pendingText.Hide()
		
		self.cancelButton = ui.Button()
		self.cancelButton.SetParent(self.board)
		self.cancelButton.SetPosition(125, 200)
		self.cancelButton.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.cancelButton.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.cancelButton.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.cancelButton.SetText("Cancel Hunt")
		self.cancelButton.SetEvent(ui.__mem_func__(self.OnClickCancel))
		self.cancelButton.Hide()
	
	def __CreateClaimableUI(self):
		self.summaryText = ui.TextLine()
		self.summaryText.SetParent(self.board)
		self.summaryText.SetFontName("Tahoma:12")
		self.summaryText.SetPosition(0, 120)
		self.summaryText.SetWindowHorizontalAlignCenter()
		self.summaryText.SetHorizontalAlignCenter()
		self.summaryText.SetText("")
		self.summaryText.Hide()
		
		self.claimButton = ui.Button()
		self.claimButton.SetParent(self.board)
		self.claimButton.SetPosition(125, 140)
		self.claimButton.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.claimButton.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.claimButton.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.claimButton.SetText("Claim Rewards")
		self.claimButton.SetEvent(ui.__mem_func__(self.OnClickClaim))
		self.claimButton.Hide()
	
	def Open(self):
		self.Show()
		self.SetCenterPosition()
		self.SetTop()
		
		# Query current state from server
		net.SendIdleHuntingQuery()
	
	def Close(self):
		self.Hide()
	
	def OnUpdate(self):
		# Called every frame - update time display
		if self.IsShow():
			self.UpdateTimeDisplay()
	
	def OnUpdateState(self, state, mob_vnum, time_left, hunt_duration, max_daily, total_today):
		"""Called when receiving packet from server"""
		self.state = state
		self.mob_vnum = mob_vnum
		self.time_left = time_left
		self.hunt_duration = hunt_duration
		self.max_daily = max_daily
		self.total_today = total_today
		
		self.RefreshUI()
	
	def RefreshUI(self):
		# Hide all state-specific UI
		for btn in self.mobButtons:
			btn.Hide()
		if self.pendingText:
			self.pendingText.Hide()
		if self.cancelButton:
			self.cancelButton.Hide()
		if self.summaryText:
			self.summaryText.Hide()
		if self.claimButton:
			self.claimButton.Hide()
		
		# Show appropriate UI for current state
		if self.state == 0 and self.mob_vnum > 0:
			# Pending: Hunt queued, waiting for logout
			self.ShowPendingState()
		elif self.state == 0:
			# Idle: No hunt active
			self.ShowMobSelection()
		elif self.state == 1:
			# Active: Hunt in progress (shouldn't see this while logged in)
			self.ShowActiveState()
		elif self.state == 2:
			# Claimable: Rewards ready
			self.ShowClaimableState()
		
		# Update time display
		self.UpdateTimeDisplay()
		self.UpdateProgressBar()
	
	def ShowMobSelection(self):
		self.stateText.SetText("Select an expedition")
		for btn in self.mobButtons:
			btn.Show()
	
	def ShowPendingState(self):
		mob_name = "Unknown"
		if self.mob_vnum in MOB_LIST:
			mob_name = MOB_LIST[self.mob_vnum]["name"]
		
		self.stateText.SetText("Hunting: %s" % mob_name)
		self.pendingText.Show()
		self.cancelButton.Show()
	
	def ShowActiveState(self):
		mob_name = "Unknown"
		if self.mob_vnum in MOB_LIST:
			mob_name = MOB_LIST[self.mob_vnum]["name"]
		
		self.stateText.SetText("Currently Hunting: %s" % mob_name)
		# No buttons shown during active hunt (shouldn't happen while logged in)
	
	def ShowClaimableState(self):
		hours = self.hunt_duration // 3600
		mins = (self.hunt_duration % 3600) // 60
		
		self.stateText.SetText("Hunt Complete!")
		self.summaryText.SetText("Hunted for %dh %dm" % (hours, mins))
		self.summaryText.Show()
		self.claimButton.Show()
	
	def UpdateTimeDisplay(self):
		used_hours = self.total_today // 3600
		used_mins = (self.total_today % 3600) // 60
		max_hours = self.max_daily // 3600
		
		if self.total_today == 0:
			self.timeText.SetText("Daily Limit: %dh" % max_hours)
		else:
			self.timeText.SetText("Daily Time: %dh %dm / %dh" % (used_hours, used_mins, max_hours))
	
	def UpdateProgressBar(self):
		if self.max_daily > 0:
			remaining = self.max_daily - self.total_today
			progress = float(remaining) / float(self.max_daily)
			self.progressBar.SetPercentage(int(progress * 100), 100)
			self.progressBar.Show()
		else:
			self.progressBar.Hide()
	
	def OnClickMob(self, group_id):
		# Send start hunting packet
		net.SendIdleHuntingStart(group_id)
	
	def OnClickCancel(self):
		net.SendIdleHuntingStop()
	
	def OnClickClaim(self):
		net.SendIdleHuntingClaim()
	
	def OnPressEscapeKey(self):
		self.Close()
		return True

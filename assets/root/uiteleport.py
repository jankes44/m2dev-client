import wndMgr,ui,grp,event

class TeleportWindow(ui.Window):
	
	def __init__(self):
		ui.Window.__init__(self,"TOP_MOST")
		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetPosition(0,0)
		self.Hide()
		self.Index = 0
		self.SendToServer = 0
		self.Loaded = 0
		
	def initData(self):
		if self.Loaded > 0:
			self.Show()
			return
		
		self.Loaded = 1
		
		self.Background = ui.Bar()
		self.Background.SetParent(self)
		self.Background.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.Background.SetPosition(0,0)
		self.Background.SetColor(grp.GenerateColor(0.0,0.0,0.0,150.0/255.0))
		self.Background.Show()
		self.MainImage = ui.ImageBox()
		self.MainImage.SetParent(self.Background)
		self.MainImage.LoadImage("uiteleport/main.tga")
		self.MainImage.SetSize(642,600)
		self.MainImage.SetCenterPosition()
		self.MainImage.Show()
		
		self.CloseButton = ui.Button()
		self.CloseButton.SetParent(self)
		self.CloseButton.SetPosition(wndMgr.GetScreenWidth()/2-350, wndMgr.GetScreenHeight()/2+200)
		self.CloseButton.SetUpVisual("uiteleport/close_n.tga")
		self.CloseButton.SetOverVisual("uiteleport/close_h.tga")
		self.CloseButton.SetDownVisual("uiteleport/close_a.tga")
		self.CloseButton.SetEvent(ui.__mem_func__(self.Open))
		self.CloseButton.Show()
		
		self.MapName = ui.ImageBox()
		self.MapName.SetParent(self)
		self.MapName.SetPosition(wndMgr.GetScreenWidth()/2+300, wndMgr.GetScreenHeight()/2+200)
		self.MapName.LoadImage("uiteleport/info.tga")
		self.MapName.SetSize(162,50)
		self.MapName.Hide()
		
		self.MapNameText = ui.TextLine()
		self.MapNameText.SetParent(self.MapName)
		self.MapNameText.SetHorizontalAlignCenter()
		self.MapNameText.SetPosition(81,18)
		self.MapNameText.SetText("PenisMap")
		self.MapNameText.Show()

		points = [[72,82],[94,172],[52,257],[124,232],[239,204],[301,153],[70,307],[157,326],[198,282],[322,199],[365,178],[419,98],[484,120],[540,153],[539,221],[454,199],[415,237],[452,261],[447,297],[457,365],[499,377],[517,412],[435,442],[368,497],[404,545],[258,370],[201,397],[304,282],[419,361],[367,300],[503,250]]
		self.data = []
		for pos in xrange(len(points)):
			button = ui.Button()
			button.SetParent(self.MainImage)
			button.SetPosition(points[pos][0],points[pos][1])
			button.SetUpVisual("uiteleport/click_n.tga")
			button.SetOverVisual("uiteleport/click_h.tga")
			button.SetDownVisual("uiteleport/click_a.tga")
			button.SetEvent(ui.__mem_func__(self.WarpPosition),pos)
			button.Show()
			self.data.append(button)
		self.Show()
		
	def UpdateIndex(self, idx):
		self.Index = idx
		
	def WarpPosition(self, arg):
		if self.Index == 0:
			return
		self.SendToServer = arg
		event.QuestButtonClick(self.Index)
		
		
	def OnUpdate(self):
		is_in = FALSE
		for i in xrange(len(self.data)):
			if self.data[i].IsIn():
				is_in = TRUE
				if not self.MapName.IsShow():
					self.UpdateMapName(i)
					self.MapName.Show()
		if not is_in and self.MapName.IsShow():
			self.MapName.Hide()
	
	def UpdateMapName(self,idx):
		mapName = ["dt","tempel","donner","rw","kap","ad","ungsam","nw","bergsohan","bakra","OT","DC","Bokjung","AD2","chunjo","nephritibuch","grotte1","grott2","boss","sd2","sd3","boss","yayang","shinsoo","ad","w�ste","schlangenfeld","jinno","feuerland","gautamakliff"]
		try:
			self.MapNameText.SetText(mapName[idx])
		except:
			pass
		
	def Open(self):
		if self.IsShow():
			self.Hide()
			return
		self.initData()
		
	def __del__(self):
		ui.Window.__del__(self)


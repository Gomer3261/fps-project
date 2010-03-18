### Director Entity ###
import base_entity

class Class(base_entity.Class):
	type = "director"
	
	def initiateGameStateData(self):
		"""
		Initiates the GameState OwnerData and ControllerData for this entity.
		"""
		import time
		
		OD = {}
		OD["gameplay"] = True
		
		CD = {}
		CD["gameTimeStart"] = time.time()
		CD["gameTime"] = 0.0
		
		self.sendData('OD', None, OD)
		self.sendData('CD', None, CD)
	
	################################################################################################
	################################################################################################
	################################################################################################
	################################################################################################
	
	def getCurrentGameTime(self):
		try:
			start = self.getCD()['gameTimeStart']
			import time
			return time.time()-start
		except:
			pass
	
	def requestSpawn(self, entityType="nanoshooter", args=[]):
		IDs = (self.Admin.UID, self.Admin.UID) # First UID needs to be the host, second UID needs to be the controller.
		memoData = ('SE', (entityType,IDs,args))
		self.sendMemo(self.EID, memoData)
		#self.Networking.gpsnet.send( ('LG', ('MEMO', (self.EID, ('SE', (entityType,IDs,args)) ) )) )
	
	def handleMemos(self):
		if self.Admin.getUID() == self.getOwner(): # Only be handling memos when we are the owner (even though the owner should be the only one who recieves memos?)
			for memo in self.memos:
				memoFlag, memoData = memo
				if memoFlag == 'SE':
					entityType, IDs, args = memoData
					self.Networking.gpsnet.send( ('GS', ('AR', ('SE', (entityType, IDs, args)))) )
			self.memos = []
	
	def userSpawnRequestControl(self):
		"""
		Allows anybody connected to this director (as a client, or owner) to send spawn requests.
		"""
		if not self.Interface.Terminal.active:
			s = self.Interface.Inputs.Controller.getStatus('spawn')
			if s==3:
				self.requestSpawn('nanoshooter') # Adding a spawn request to the respawnRequestQueue.

	################################################################################################
	################################################################################################
	################################################################################################
	################################################################################################

	def controllerDataSimulate(self): # Maybe game time stuff should be owner data? Probably doesn't matter.. I don't know...
		"""
		Simulates controller data, and updates the changes to the GameState via Networking.
		"""
		
		### Only updates the clock every second ###
		CD = self.getCD()
		if 'gameTime' in CD:
			oldGameTime = CD['gameTime']
			currentGameTime = self.getCurrentGameTime()
			difference = currentGameTime - oldGameTime
			if difference > 1.0:
				self.throwData('CD', 'gameTime', currentGameTime)
	
	
	
	
	
	
	def alwaysRun(self):
		try:
			self.userSpawnRequestControl()
		except: import traceback; traceback.print_exc()
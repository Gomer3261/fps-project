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
		CD["spawnRequestQueue"] = []
		
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
	
	def requestSpawn(self, entityType="nanoshooter"):
		self.Networking.gpsnet.send( ('GS', ('VA', (self.EID, 'CD', 'spawnRequestQueue', [entityType]))) )
	
	def handleSpawnRequests(self):
		if 'spawnRequestQueue' in self.getCD():
			spawnRequestQueue = self.getCD()['spawnRequestQueue']
			if spawnRequestQueue:
				for entityType in spawnRequestQueue:
					self.Networking.gpsnet.send( ('GS', ('AR', ('SE', (entityType, (self.Admin.UID, self.Admin.UID), [])))) )
												#   ('EM', [(EID,      type,       key,        value)])
				self.Networking.gpsnet.send( ('GS', ('EM', [(self.EID, 'CD', 'spawnRequestQueue', [])])) ) # Clearing the Queue -- XXX -- Might turn into a problem, because
				# there may be a delay in clearing the queue, which may making single items in the queue handled multiple times.... yikes.
	
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

	def controllerDataSimulate(self):
		"""
		Simulates controller data, and updates the changes to the GameState via Networking.
		"""
		self.handleSpawnRequests()
		
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
		except:
			pass
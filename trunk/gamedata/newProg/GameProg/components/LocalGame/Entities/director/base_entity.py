### Base Entity ###

class Class:
	type = "base_entity"
	
	def __init__(self, EID, LocalGame):
		self.EID = EID
		
		self.LocalGame = LocalGame
		self.Admin = LocalGame.Admin
		self.GameState = LocalGame.GameState
		self.Networking = LocalGame.Networking
		self.Interface = LocalGame.Interface
		
		if self.Admin.UID == self.getOwner():
			# We only initiate the GameState Data when we are the Owner during initiation.
			# I think that's how it should go down I guess. Not sure. :P
			self.initiateGameStateData()
	
	
	
	def initiateGameStateData(self):
		OD = {}
		CD = {}
		
		self.sendData('OD', None, OD)
		self.sendData('CD', None, CD)
	
	
	
	
	###
	### Get Data
	###
	
	def getData(self):
		return self.GameState.getEntity(self.EID)
	
	def getOwner(self):
		return self.getData()['O']
	
	def getController(self):
		return self.getData()['C']
	
	def getCD(self): # Controller Data
		return self.getData()['CD']
	
	def getOD(self): # Owner Data
		return self.getData()['OD']
	
	
	###
	### Set Data
	###
	
	def setData(self, type, key, value):
		self.Networking.gpsnet.send( ['GS', ['EM', [(self.EID, type, key, value)]]] )
	
	def sendData(self, type, key, value):
		self.Networking.gpsnet.send( ['GS', ['EM', [(self.EID, type, key, value)]]] )
	
	def throwData(self, type, key, value):
		self.Networking.gpsnet.throw( ['GS', ['EM', [(self.EID, type, key, value)]]] )
	
	
	################################################
	################################################
	################################################
	################################################
	
	def run(self):
		UID = self.Admin.getUID()
		
		if self.getOwner() == UID: self.ownerDataSimulate()
		else: self.ownerDataReplicate()
		
		if self.getController() == UID: self.controllerDataSimulate()
		else: self.controllerDataReplicate()
		
		self.alwaysRun()
	
	def alwaysRun(self):
		pass
	
	
	################################################
	################################################
	################################################
	################################################
	
	
	def ownerDataSimulate(self):
		"""
		Simulates owner data, and updates the changes to the GameState via Networking.
		"""
		pass
	
	def ownerDataReplicate(self):
		"""
		Replicates the GameState description of this entity's owner data.
		"""
		pass
	
	################################################
	################################################
	################################################
	################################################
	
	
	def controllerDataSimulate(self):
		"""
		Simulates controller data, and updates the changes to the GameState via Networking.
		"""
		pass
	
	def controllerDataReplicate(self):
		"""
		Replicates the GameState description of this entity's controller data to the local self's copy.
		"""
		pass

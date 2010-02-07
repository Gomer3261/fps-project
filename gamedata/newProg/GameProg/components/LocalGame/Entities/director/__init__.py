### Director Entity ###

class Class:
	def __init__(self, EID, LocalGame):
		self.type = "director"
		self.EID = EID
		
		self.LocalGame = LocalGame
		self.Admin = LocalGame.Admin
		self.GameState = LocalGame.GameState
		self.Networking = LocalGame.Networking
		self.Interface = LocalGame.Interface
	
	def getDescription(self):
		return self.GameState.getEntity(self.EID)
	
	def getOwner(self):
		return self.getDescription()['O']
	
	def getController(self):
		return self.getDescription()['C']
	
	
	################################################
	################################################
	################################################
	################################################
	
	def run(self):
		UID = self.Admin.getUID()
		
		if self.getOwner() == UID: ownerDataSimulate()
		else: ownerDataReplicate()
		
		if self.getController() == UID: controllerDataSimulate()
		else: controllerDataReplicate()
	
	
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

### LocalGame Component ###

class Class:
	def __init__(self):
		self.entities = {}
	
	
	# Main Loop
	def run(self, GameState, Networking, Resources):
		self.GameState = GameState
		self.Networking = Networking
		self.Resources = Resources
		
		self.replicateGameState(self.GameState)
		self.runEntities()
	
	
	# Replication
	def replicateGameState(self, GameState):
		GS_entitydict = GameState.getEntityDict()
		for EID in GS_entitydict:
			if EID not in self.entities:
				self.createEntity(EID)
	
	
	# Creating Entities
	def createEntity(self, EID):
		import Entities
		type = self.GameState.getEntityType(EID)
		self.entities[EID] = Entities.getEntityClass(type)(EID, self)
	
	
	# Running Entities
	def runEntities(self):
		for EID in self.entities:
			self.entities[EID].run(self)
		
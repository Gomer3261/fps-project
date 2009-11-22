### LocalGame Component ###

class Class:
	def __init__(self, cont=None):
		self.entities = {}
	
	
	# Main Loop
	def run(self, GameState, Networking):
		self.GameState = GameState
		self.Networking = Networking
		
		self.replicateGameState(self.GameState)
		self.runEntities()
	
	
	# Replication
	def replicateGameState(self, GameState):
		GS_entitydict = GameState.getEntityDict()
		for ID in GS_entitydict:
			if ID not in self.entities:
				self.createEntity(ID)
	
	
	# Creating Entities
	def createEntity(self, ID):
		import Entities
		type = self.GameState.getEntityType(ID)
		self.entities[ID] = Entities.getEntityClass(type)(ID, self)
	
	
	# Running Entities
	def runEntities(self):
		for ID in self.entities:
			self.entities[ID].run(self)
		
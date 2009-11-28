### LocalGame Component ###

class Class:
	def __init__(self):
		self.entities = {}
	
	
	# Main Loop
	def run(self, GameState, Networking, Resources, Interface):
		self.GameState = GameState
		self.Networking = Networking
		self.Resources = Resources
		self.Interface = Interface
		
		self.replicateGameState(self.GameState)
		self.runEntities()
	
	
	# Replication
	def replicateGameState(self, GameState):
		for EID in GameState.contents["E"]:
			if EID not in self.entities:
				self.createEntity(EID)
	
	
	# Creating Entities
	def createEntity(self, EID):
		import Entities
		type = self.GameState.getEntity(EID)['T']
		self.entities[EID] = Entities.getEntityClass(type)(EID, self)
	
	
	# Running Entities
	def runEntities(self):
		for EID in self.entities:
			self.entities[EID].run()

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
		# Adding entities that are described in GameState but are not in LocalGame.entities.
		try:
			for EID in GameState.contents["E"]:
				if EID not in self.entities:
					self.createEntity(EID)
		except:
			pass
		
		# Deleting entities that are in LocalGame.entities but not in GameState.
		try:
			for EID in self.entities:
				if EID not in GameState.contents['E']:
					self.removeEntity(EID)
		except:
			pass
	
	# Creating Entities
	def createEntity(self, EID):
		import Entities
		type = self.GameState.getEntity(EID)['T']
		self.entities[EID] = Entities.getEntityClass(type)(EID, self)
	
	# Removing Entities
	def removeEntity(self, EID):
		self.entities[EID].end()
		del self.entities[EID]
	
	
	# Running Entities
	def runEntities(self):
		for EID in self.entities:
			self.entities[EID].run()

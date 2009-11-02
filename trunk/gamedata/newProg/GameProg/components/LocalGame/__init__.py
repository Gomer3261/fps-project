### LocalGame Component ###

class Class:
	def __init__(self, cont):
		self.entities = {}
		
	def run(self, GameState):
		self.replicate(GameState)
		self.runEntities()
	
	def replicate(self, GameState):
		for EID in GameState.contents["E"]: # Looping through each entity in the GameState
			GameStateInfo = GameState.contents["E"][EID]
			
			if EID not in self.entities:
				import entities
				# Spawn the entity.
				type = GameStateInfo['T']
				entityObject = entities.spawnEntity(type)
				self.entities[EID] = entityObject
				print("Entity Added")
	
	def runEntities(self):
		for EID in self.entities:
			entity = self.entities[EID]
			entity.run()

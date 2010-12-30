# Entities

class initializeEntityController:
	def __init__(self):
		self.entities = {}
		self.entityClasses = {}
		
		import engine.entities.baseEntity; self.entityClasses["baseEntity"] = baseEntity.Class
		import engine.entities.cube; self.entityClasses["cube"] = cube.Class
		import engine.entities.director; self.entityClasses["director"] = director.Class

	def conform(self, gamestate ):
		delete = []
		for id in self.entities:
			if not id in gamestate["E"]:
				self.entities[id].end()
				delete.append(id)
				
		for i in delete:
			del self.entities[i]

		for id in gamestate["E"]:
			if id not in self.entities:
				self.entities[id] = self.createEntity( id, gamestate )
				
	def createEntity(self, id, gamestate):
		return self.entityClasses[gamestate["E"][id]["t"]]( id, gamestate, self )
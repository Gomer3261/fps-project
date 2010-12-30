# Entities

class initiateEntityController:
	def __init__(self):
		self.entities = {}
		self.entityClasses = {}
		
		import engine.entities.base_entity; self.entityClasses["base_entity"] = base_entity.Class

	def conform(self, gamestate ):
		delete = []
		for id in self.entities:
			if id not in gamestate["E"]:
				self.entities[id].end()
				delete.append(id)
				
		for i in delete:
			del self.entities[i]

		for id in gamestate["E"]:
			if id not in self.entities:
				self.entities[id] = self.createEntity( id, gamestate )
				
	def createEntity(self, id, gamestate):
		return self.entityClasses[gamestate["E"][id]["type"]]( id, gamestate, self )
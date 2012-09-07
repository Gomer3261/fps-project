# Entities

class createEntityController:
	def __init__(self):
		self.entities = {}
		self.entityClasses = {}
		
		import engine.entities.baseEntity; self.entityClasses["baseEntity"] = baseEntity.Class
		import engine.entities.cube; self.entityClasses["cube"] = cube.Class
		import engine.entities.director; self.entityClasses["director"] = director.Class
		import engine.entities.player; self.entityClasses["player"] = player.Class
	
	def submitMemos(self, memos):
		for memoItem in memos:
			id, memo = memoItem
			self.entities[id].memoInbox.append(memo)

	def conform(self, gamestate):
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
		
		
	def importCurrentScene(self, gamestate):
		import bge;
		import engine;
		
		for object in bge.logic.getCurrentScene().objects:
			if "type" in object:
				if object["type"] in self.entityClasses and engine.host:
					id =  gamestate.addEntity(object["type"])
					if(id):
						self.entities[id] = self.entityClasses[object["type"]]( id, gamestate, self, object )
					else:
						object.endObject()
				else:
					object.endObject()

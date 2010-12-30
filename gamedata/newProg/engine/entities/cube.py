# Entities

class Class:
	def __init__(self, id, gamestate, entityController):
		import engine
		self.engine = engine
		self.id = id
		self.entityController = entityController
		
		if gamestate.hasControl(self.id): self.initiateGamestateData( gamestate )
		
		self.initiate( gamestate )
		
	def initiateGamestateData(self, gamestate):
		data = {}
		delta = {'E':{self.id:data}}
		gamestate.mergeDelta(delta)
	
	def initiate(self, gamestate):
		import bge
		self.object = bge.logic.getCurrentScene().addObject("cube", bge.logic.getCurrentController().owner)
		#Create game objects and such here. Remember to you import bge
		
	def end():
		self.object.end()
		#Remove game objects and handle any deconstruction methods/issues
	
	def run(self, gamestate):
		if gamestate.hasControl(self.id):
			self.controllerDataSimulate()
		else:
			self.controllerDataReplicate()
		
		if self.engine.host:
			self.serverDataSimulate()
		else:
			self.serverDataReplicate()
		return None, None
		
	def serverDataSimulate(self):
		pass
	
	def serverDataReplicate(self):
		pass
	
	def controllerDataSimulate(self):
		pass
	
	def controllerDataReplicate(self):
		pass

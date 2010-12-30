# Director Class

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
		data['count'] = 0
		delta = {'E':{self.id:data}}
		gamestate.mergeDelta(delta)
	
	def initiate(self, gamestate):
		import bge
		self.object = bge.logic.getCurrentScene().addObject("cube", bge.logic.getCurrentController().owner)
		self.count = 0
		#Create game objects and such here. Remember to you import bge
		
	def end(self):
		self.object.endObject()
		#Remove game objects and handle any deconstruction methods/issues
	
	def run(self, gamestate):
		if gamestate.hasControl(self.id):
			self.controllerDataSimulate(gamestate)
		else:
			self.controllerDataReplicate(gamestate)
		
		if self.engine.host:
			self.serverDataSimulate(gamestate)
		else:
			self.serverDataReplicate(gamestate)
		return None, None
		
	def serverDataSimulate(self, gamestate):
		self.count+=1
		data = {}
		data['count'] = self.count
		delta = {'E':{self.id:data}}
		if self.count >= 100:
			delta['E'][self.id] = None
		gamestate.mergeDelta(delta)
	
	def serverDataReplicate(self, gamestate):
		pass
	
	def controllerDataSimulate(self, gamestate):
		pass
	
	def controllerDataReplicate(self, gamestate):
		pass

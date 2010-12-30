# Entities

class Class:
	def __init__(self, id, gamestate, entityController):
		self.id = id
		self.entityController = entitiyController
		
		if self.controller: self.initiateGamestateData( gamestate )
		
		self.initiate( gamestate )
		
	def initiateGamestateData(self, gamestate):
		data = {}
		delta = {'E':{self.id:data}}
		gamestate.mergeDelta(delta)
	
	def initiate(self, gamestate):
		pass
		#Create game objects and such here. Remember to you import bge
		
	def end():
		pass
		#Remove game objects and handle any deconstruction methods/issues
	
	def run(self, gamestate):
		if gamestate.hasControl(self.id):
			self.controllerDataSimulate()
		else:
			self.controllerDataReplicate()
		
		if gamestate.host:
			self.serverDataSimulate()
		else:
			self.serverDataReplicate()
		
	def serverDataSimulate(self):
		pass
	
	def serverDataReplicate(self):
		pass
	
	def controllerDataSimulate(self):
		pass
	
	def controllerDataReplicate(self):
		pass

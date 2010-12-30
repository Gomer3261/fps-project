# Base Entity

class Class:
	def __init__(self, id, gamestate, entityController):
		self.id = id
		self.entityController = entityController
		import engine; self.engine = engine
		
		if gamestate.hasControl(self.id): self.initializeGamestateData( gamestate )
		
		self.initialize( gamestate )
	
	### 
	### __init__ function is supposed to remain uniform across all entities.
	### 
	
	
	
	
	
	
	def initializeGamestateData(self, gamestate):
		data = {'key':'value'}
		#delta = {'E':{self.id:data}} # Putting it in gamestate.delta form
		#gamestate.mergeDelta(delta) # merging it with gamestate's delta
	
	def initialize(self, gamestate):
		"""
		Custom initialization for this entity object.
		Often involves creating a bge object.
		"""
		pass
		#import bge
		#self.object = bge.logic.getCurrentScene().addObject("cube", bge.logic.getCurrentController().owner)
		
	def end(self):
		"""
		Mandatory end method, often involves deleting bge object.
		"""
		pass
		#self.object.endObject()
	
	def serverDataSimulate(self, gamestate):
		"""
		Simulates stuff, and returns gamestate delta data to the
		mainloop, where it is merged with the gamestate delta.
		"""
		return None # Return delta data to be merged with gamestate.delta
	
	def serverDataReplicate(self, gamestate):
		pass
	
	def controllerDataSimulate(self, gamestate):
		"""
		Simulates stuff, and returns gamestate delta data to the
		mainloop, where it is merged with the gamestate delta.
		"""
		return None # Return delta data to be merged with gamestate.delta
	
	def controllerDataReplicate(self, gamestate):
		pass
	
	
	
	
	
	
	### 
	### Run function is supposed to remain uniform across all entities.
	### 
	
	def run(self, gamestate):
		"""
		Runs the four basic methods that make entities do stuff.
		Returns delta data sets to the mainloop.
		"""
		deltaDataList = []
		if gamestate.hasControl(self.id):
			deltaDataList.append( self.controllerDataSimulate(gamestate) )
		else:
			self.controllerDataReplicate(gamestate)
		
		if self.engine.host:
			deltaDataList.append( self.serverDataSimulate(gamestate) )
		else:
			self.serverDataReplicate(gamestate)
		return deltaDataList

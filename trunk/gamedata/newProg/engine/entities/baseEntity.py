# Base Entity

class Class:
	def __init__(self, id, gamestate, entityController):
		self.id = id
		self.entityController = entityController
		import engine; self.engine = engine
		import time; self.time=time
		
		self.control = gamestate.hasControl(self.id)
		
		self.memos = [] # list of incoming memos.
		
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
		self.object.endObject()
	
	
	
	# The four fundamental run functions
	
	def simulateServerData(self, gamestate):
		"""
		Simulates stuff, and returns gamestate delta data to the
		mainloop, where it is merged with the gamestate delta.
		Memos are handled by this method.
		"""
		# Handle memos before clearing them each run.
		self.memos = [] # Clear memos when you're done with them.
		return [] # Return delta data to be merged with gamestate.delta
	
	def replicateServerData(self, gamestate):
		"""
		This is where memos are born. Memos are messages to serverside entities.
		"""
		memos = []
		id=None; data=None
		memo=(id,data)
		return memos
	
	def simulateControllerData(self, gamestate):
		"""
		Simulates stuff, and returns gamestate delta data to the
		mainloop, where it is merged with the gamestate delta.
		"""
		return [] # Return delta data to be merged with gamestate.delta
	
	def replicateControllerData(self, gamestate):
		pass
	
	
	
	
	
	
	### 
	### Run function is supposed to remain uniform across all entities.
	### 
	
	def run(self, gamestate):
		"""
		Runs the four basic methods that make entities do stuff.
		Returns delta data sets to the mainloop.
		"""
		deltaDataList=[]; memoList=[]
		if gamestate.hasControl(self.id):
			deltas = self.simulateControllerData(gamestate)
			for delta in deltas: deltaDataList.append(delta)
		else:
			self.replicateControllerData(gamestate)
		
		if self.engine.host:
			deltas = self.simulateServerData(gamestate)
			for delta in deltas: deltaDataList.append(delta)
		else:
			memoList = self.replicateServerData(gamestate)
		return deltaDataList, memoList

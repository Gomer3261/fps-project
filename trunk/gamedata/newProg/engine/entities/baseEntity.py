# Base Entity

class Class:
	def __init__(self, id, gamestate, entityController, gameObject=None):
		self.id = id
		self.entityController = entityController
		import engine; self.engine = engine
		import time; self.time=time
		import bge; self.bge=bge
		
		self.control = gamestate.hasControl(self.id)
		
		self.memoInbox = [] # list of incoming memos.
		self.memoOutbox = [] # list of outgoing memos.
		self.deltaOutbox = [] # list of outgoing deltas. 
		
		if gamestate.hasControl(self.id): self.initializeGamestateData( gamestate )
		self.initialize( gamestate, gameObject )
		
	def run(self, gamestate):
		self.memoOutbox = [] # list of outgoing memos.
		self.deltaOutbox = [] # list of outgoing deltas. 
		
		### host/client ###
		if self.engine.host:
			self.host(gamestate)
		else:
			self.client(gamestate)
		### controller/proxy ###
		if gamestate.hasControl(self.id):
			self.controller(gamestate)
		else:
			self.proxy(gamestate)
		return self.deltaOutbox, self.memoOutbox # Returns delta data and memos.
	
	def submitDelta(self, delta): self.deltaOutbox.append(delta)
	def submitMemo(self, memo): self.memoOutbox.append(memo) # (toEntityId, memoData)
	
	##########################################################################
	############    • CODE ABOVE IS UNIFORM AMONG ALL ENTITIES    ############
	############    • CODE BELOW IS ENTITY-SPECIFIC               ############
	##########################################################################

	def initializeGamestateData(self, gamestate):
		pass
		#data = {'key':'value'}
		#delta = {'E':{self.id:data}} # Putting it in gamestate.delta form
		#gamestate.mergeDelta(delta) # merging it with gamestate's delta
	
	def initialize(self, gamestate, gameObject):
		# Custom initialization for this entity; often includes creating a bge object.
		# The game object parameter allows an existing game object to be passed into the engine for proper incorperation.
		if(gameObject):
			gameObject.endObject()
		#import bge
		#self.object = bge.logic.getCurrentScene().addObject("cube", bge.logic.getCurrentController().owner)
		#print("RUNNING")
		#print(self.id)
		
	def end(self):
		# End method, often involves deleting bge object.
		pass
		#self.object.endObject()
	
	
	############################################
	############ THE FANTASTIC FOUR ############
	############################################
	
	#================#
	#===== HOST =====# Server-side behaviour for this entity.
	#================# Updates server-data
	def host(self, gamestate):
		self.hosthandleMemos()
	
	#---------#
	#- MEMOS -# Server-side memo handling for this entity.
	#---------# This method is a part of the host method.
	def hostHandleMemos(self):
		self.memoInbox = []
		#for memo in self.memoInbox:
		#	pass # Handle each memo.
	
	#==================#
	#===== CLIENT =====# Client-side behaviour for this entity.
	#==================# Replicates server-data.
	def client(self, gamestate):
		pass
	
	#======================#
	#===== CONTROLLER =====# Controller behaviour for this entity.
	#======================# Updates controller-data; creates memos.
	def controller(self, gamestate):
		pass
	
	#=================#
	#===== PROXY =====# Proxy behaviour for this entity.
	#=================# Replicates controller-data.
	def proxy(self, gamestate):
		pass
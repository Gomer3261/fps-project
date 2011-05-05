# Cube Entity
import engine.entities.baseEntity as baseEntity
class Class(baseEntity.Class):

	def initializeGamestateData(self, gamestate):
		data = {}
		data['count'] = 0
		delta = {'E':{self.id:data}}
		gamestate.mergeDelta(delta)
	
	def initialize(self, gamestate):
		import bge
		self.object = bge.logic.getCurrentScene().addObject("cube", bge.logic.getCurrentController().owner)
		self.count = 0
	
	def host(self, gamestate):
		self.count+=1
		if self.count >= 100:
			self.submitDelta( {'E':{self.id:None}} )
			
	
	


	def initializeGamestateData(self, gamestate):
		data = {'count':'0'}
		delta = {'E':{self.id:data}} # Putting it in gamestate.delta form
		gamestate.mergeDelta(delta) # merging it with gamestate's delta
	
	def initialize(self, gamestate):
		# Custom initialization for this entity; often includes creating a bge object.
		import bge
		self.object = bge.logic.getCurrentScene().addObject("cube", bge.logic.getCurrentController().owner)
		self.count = 0
		
	def end(self):
		# End method, often involves deleting bge object.
		self.object.endObject()
	
	
	########################################################
	############ THE FANTASTIC FOUR RUN METHODS ############
	########################################################
	
	#================#
	#===== HOST =====# Server-side behaviour for this entity.
	#================# Defines server-data; handles memos.
	def host(self, gamestate):
		self.count+=1
		if self.count >= 100: self.submitDelta( {'E':{self.id:None}} )
		
		host_handleMemos()
	def host_handleMemos(self):
		for memo in self.memoInbox:
			pass # Handle each memo.
		self.memoInbox = []
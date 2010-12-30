# Base Entity
import engine.entities.baseEntity as baseEntity
class Class(baseEntity.Class):

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
		import engine
		import bge
		keyboard = bge.logic.keyboard

		if keyboard.events[bge.events.QKEY] == 3:
			return {'E':{gamestate.getNextId():{'t':'cube','c':engine.id}}}
		
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

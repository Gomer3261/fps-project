# Cube Entity
import engine.entities.baseEntity as baseEntity
class Class(baseEntity.Class):

	def initializeGamestateData(self, gamestate):
		data = {}
		data['count'] = 0
		delta = {'E':{self.id:data}}
		gamestate.mergeDelta(delta)
	
	def initialize(self, gamestate):
		"""
		Custom initialization for this entity object.
		Often involves creating a bge object.
		"""
		import bge
		self.object = bge.logic.getCurrentScene().addObject("cube", bge.logic.getCurrentController().owner)
		self.count = 0
		
	def end(self):
		"""
		Mandatory end method, often involves deleting bge object.
		"""
		self.object.endObject()
	
	def serverDataSimulate(self, gamestate):
		"""
		Simulates stuff, and returns gamestate delta data to the
		mainloop, where it is merged with the gamestate delta.
		"""
		self.count+=1
		data = {}
		data['count'] = self.count
		delta = {'E':{self.id:data}}
		if self.count >= 100:
			delta['E'][self.id] = None
		return delta # Return delta data to be merged with gamestate.delta
	
	def controllerDataSimulate(self, gamestate):
		"""
		Simulates stuff, and returns gamestate delta data to the
		mainloop, where it is merged with the gamestate delta.
		"""
		return None # Return delta data to be merged with gamestate.delta
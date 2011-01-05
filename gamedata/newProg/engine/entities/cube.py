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
	
	def serverDataSimulate(self, gamestate):
		"""
		Simulates stuff, and returns gamestate delta data to the
		mainloop, where it is merged with the gamestate delta.
		"""
		deltas = []
		self.count+=1
		if self.count >= 100:
			deltas.append( {'E':{self.id:None}} )
		return deltas # Return delta data to be merged with gamestate.delta
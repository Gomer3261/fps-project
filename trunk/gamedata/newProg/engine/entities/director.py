# Base Entity
import engine.entities.baseEntity as baseEntity
class Class(baseEntity.Class):

	def simulateServerData(self, gamestate):
		"""
		Simulates stuff, and returns gamestate delta data to the
		mainloop, where it is merged with the gamestate delta.
		"""
		deltas = []
		
		import engine
		import bge
		keyboard = bge.logic.keyboard
		
		if keyboard.events[bge.events.PKEY] == 3 and (not engine.interface.terminalIsActive()):
			if not gamestate.hasEntity(engine.id, 'player'): 
				deltas.append( {'E':{gamestate.getNextId():{'t':'player','c':engine.id}}} )
		
		for memo in self.memos:
			type, controlId = memo
			if type=='player' and gamestate.hasEntity(controlId, type): continue
			deltas.append( {'E':{gamestate.getNextId():{'t':type,'c':controlId}}} )
		self.memos = [] # Clearing memos.
		
		return deltas # Return delta data to be merged with gamestate.delta
	
	def replicateServerData(self, gamestate):
		memos = []
		
		import engine
		import bge
		keyboard = bge.logic.keyboard
		if keyboard.events[bge.events.PKEY] == 3 and (not engine.interface.terminalIsActive()):
			memos.append( (self.id, ('player', self.engine.id)) )
		
		return memos # Return memos.
	
	def simulateControllerData(self, gamestate):
		"""
		Simulates stuff, and returns gamestate delta data to the
		mainloop, where it is merged with the gamestate delta.
		"""
		return [] # Return delta data to be merged with gamestate.delta
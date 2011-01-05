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
		
		if keyboard.events[bge.events.QKEY] == 3 and (not engine.interface.terminalIsActive()):
			deltas.append( {'E':{gamestate.getNextId():{'t':'player','c':engine.id}}} )
		
		for memo in self.memos:
			print("\nServerside Director Recieved Memo!", memo, '\n')
			if memo == "spawn cube plz":
				deltas.append( {'E':{gamestate.getNextId():{'t':'cube','c':engine.id}}} )
		self.memos = [] # Clearing memos.
		
		return deltas # Return delta data to be merged with gamestate.delta
	
	def replicateServerData(self, gamestate):
		memos = []
		
		import engine
		import bge
		keyboard = bge.logic.keyboard
		if keyboard.events[bge.events.QKEY] == 3 and (not engine.interface.terminalIsActive()):
			memos.append( (self.id, "spawn cube plz") )
		
		return memos # Return memos.
	
	def simulateControllerData(self, gamestate):
		"""
		Simulates stuff, and returns gamestate delta data to the
		mainloop, where it is merged with the gamestate delta.
		"""
		return [] # Return delta data to be merged with gamestate.delta
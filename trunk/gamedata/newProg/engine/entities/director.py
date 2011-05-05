# Base Entity
import engine.entities.baseEntity as baseEntity
class Class(baseEntity.Class):

	##################
	###### HOST ###### Server-side behaviour for this entity.
	################## Defines server-data; handles memos.
	def host(self, gamestate):	
		import engine
		import bge
		keyboard = bge.logic.keyboard
		
		if keyboard.events[bge.events.PKEY] == 3 and (not engine.interface.terminalIsActive()):
			if not gamestate.hasEntity(engine.id, 'player'): 
				self.submitDelta( {'E':{gamestate.getNextId():{'t':'player','c':engine.id}}} )
	
	def hostHandleMemos(self):
		for memo in self.memoInbox:
			type, controlId = memo
			if type=='player' and gamestate.hasEntity(controlId, type): continue
			self.submitDelta( {'E':{gamestate.getNextId():{'t':type,'c':controlId}}} )
	
	####################
	###### CLIENT ###### Client-side behaviour for this entity.
	#################### Replicates server-data.
	def client(self, gamestate):		
		import engine
		import bge
		keyboard = bge.logic.keyboard
		if keyboard.events[bge.events.PKEY] == 3 and (not engine.interface.terminalIsActive()):
			self.submitMemo( (self.id, ('player', self.engine.id)) )
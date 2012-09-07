# Base Entity
import engine.entities.baseEntity as baseEntity
class Class(baseEntity.Class):

	#================#
	#===== HOST =====# Server-side behaviour for this entity.
	#================# Updates server-data
	def host(self, gamestate):
		
		keyboard = self.bge.logic.keyboard
		if keyboard.events[self.bge.events.PKEY] == 3 and (not self.engine.interface.terminalIsActive()):
			self.submitMemo( (self.id, ('player', self.engine.id)) )
		
		self.hostHandleMemos()
	
	#---------#
	#- MEMOS -# Server-side memo handling for this entity.
	#---------# This method is a part of the host method.
	def hostHandleMemos(self):
		
		for memo in self.memoInbox:
			type, controlId = memo
			if controlId == None: controlId = self.engine.id
			if(self.engine.gamestate.containsUser(controlId)):
				if type=='player' and self.engine.gamestate.hasEntity(controlId, type): continue
				self.submitDelta( {'E':{self.engine.gamestate.getNextId():{'t':type,'c':controlId}}} )
			
		self.memoInbox = []
	
	#==================#
	#===== CLIENT =====# Client-side behaviour for this entity.
	#==================# Replicates server-data.
	def client(self, gamestate):		
		
		keyboard = self.bge.logic.keyboard
		if keyboard.events[self.bge.events.PKEY] == 3 and (not self.engine.interface.terminalIsActive()):
			self.submitMemo( (self.id, ('player', self.engine.id)) )
			
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

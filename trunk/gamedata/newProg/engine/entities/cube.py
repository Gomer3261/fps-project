# Cube Entity
import engine.entities.baseEntity as baseEntity
class Class(baseEntity.Class):

	def initializeGamestateData(self, gamestate):
		data = {}
		data['P'] = [0.0, 0.0, 0.0] # Position
		data['H'] = 100
		delta = {'E':{self.id:data}}
		gamestate.mergeDelta(delta)
	
	def initialize(self, gamestate, gameObject):
		if(self.engine.host):
			self.lastUpdate = self.time.time()
			self.updateInterval = 0.1 
		
		if(gameObject and self.engine.host):
			self.object = gameObject
		else:
			self.object = self.bge.logic.getCurrentScene().addObject("cube", self.bge.logic.getCurrentController().owner)
		
		self.hp = 100;
		self.object["id"] = self.id
		self.object["hp"] = self.hp
		self.object["targetable"] = True
		
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
		
		if self.time.time()-self.lastUpdate > self.updateInterval:
			pos = [0.0, 0.0, 0.0]
			for i in range(3): pos[i]=str(round(self.object.worldPosition[i], 3))
			self.submitDelta( {'E': {self.id:{'P':pos}} } )
			self.lastUpdate = self.time.time()
		
		data = self.hostHandleMemos()
		
		if(data):
			self.submitDelta( {'E':data} )
		
	#---------#
	#- MEMOS -# Server-side memo handling for this entity.
	#---------# This method is a part of the host method.
	def hostHandleMemos(self):
		data = None

		for memo in self.memoInbox:
			if(memo[0] == "dmg"):
				dmg = memo[1]
				self.hp -= dmg
				self.object["hp"] = self.hp
				if(self.hp <= 0):
					data = {self.id:None}
					break;
				else:
					data = {self.id:{'H':self.hp}}
			
		self.memoInbox = []
		return data
		
	#==================#
	#===== CLIENT =====# Client-side behaviour for this entity.
	#==================# Replicates server-data.
	def client(self, gamestate):
		data = self.engine.gamestate.getById(self.id)
		if 'P' in data:
			pos = data['P']
			for i in range(3): pos[i]=float(pos[i])
			self.object.worldPosition = pos
		if 'H' in data:
			self.hp = data['H']
			self.object["hp"] = self.hp 
	
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
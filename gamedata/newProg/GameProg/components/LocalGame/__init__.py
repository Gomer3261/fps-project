### LocalGame Component ###

class Class:
	def __init__(self, slab):
		import Camera as CameraMod; self.Camera = CameraMod.Class()
		import RequestHandler as RequestHandlerMod; self.RequestHandler = RequestHandlerMod.Class()
		import Entities; self.EntityModule = Entities
		
		self.entities = {}
		print("LocalGame's good to go.")
	
	
	# Main Loop
	def run(self, Admin, GameState, Network, Resources, Interface):
		self.Admin = Admin
		self.GameState = GameState
		self.Network = Network
		self.Resources = Resources
		self.Interface = Interface
		
		self.RequestHandler.run(self, self.Network)
		self.replicateGameState(self.GameState)
		self.runEntities()
	
	
	def giveMemo(self, EID, memoData):
		try:
			if EID:
				if not EID in self.entities: raise(Exception, "Memo Error: EID not in LocalGame.entities?")
				entity = self.entities[EID]
				entity.memos.append(memoData)
			else:
				raise(Exception, "Memo Error: no EID given.")
		except: import traceback; traceback.print_exc()
	
	
	# Replication
	def replicateGameState(self, GameState):
		# Adding entities that are described in GameState but are not in LocalGame.entities.
		try:
			for EID in GameState.contents["E"]:
				if EID not in self.entities:
					self.createEntity(EID)
		except:
			import traceback; traceback.print_exc()
			pass
		
		# Deleting entities that are in LocalGame.entities but not in GameState.
		try:
			toRemove = []
			for EID in self.entities:
				if EID not in GameState.contents['E']:
					toRemove.append(EID)
			for EID in toRemove:
				self.removeEntity(EID)
		except:
			import traceback; traceback.print_exc()
			pass
	
	# Creating Entities
	def createEntity(self, EID):
		type = self.GameState.getEntity(EID)['T']
		self.entities[EID] = self.EntityModule.getEntityClass(type)(EID, self)
	
	def getEntityClass(self, type):
		return self.EntityModule.getEntityClass(type)
	
	def getEntity(self, EID):
		if EID in self.entities: return self.entities[EID]
		else: return None
	
	def getEntitiesByType(self, type):
		result = []
		for EID in self.entities:
			entity = self.entities[EID]
			if entity.type == type: result.append(EID)
		return result
	
	# Removing Entities
	def removeEntity(self, EID):
		self.entities[EID].end()
		del self.entities[EID]
	
	
	# Running Entities
	def runEntities(self):
		for EID in self.entities:
			try:
				self.entities[EID].run()
			except:
				import traceback
				print("\nError in entity %s (%s):" % (EID, self.entities[EID].type))
				traceback.print_exc()
				print(" ")




### LocalGame Component ###

class Class:
	def __init__(self, slab):
		import Camera as CameraMod; self.Camera = CameraMod.Class()
		import RequestHandler as RequestHandlerMod; self.RequestHandler = RequestHandlerMod.Class()
		
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
		self.removeEntitiesWithNonExistantUsers()
	
	
	def giveMemo(self, EID, memoData):
		try:
			if EID:
				if not EID in self.entities: raise Exception, "Memo Error: EID not in LocalGame.entities?"
				entity = self.entities[EID]
				entity.memos.append(memoData)
			else:
				raise Exception, "Memo Error: no EID given."
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
		import Entities
		type = self.GameState.getEntity(EID)['T']
		self.entities[EID] = Entities.getEntityClass(type)(EID, self)
	
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
	
	# Remove entities with non-existant users as controller/owner
	def removeEntitiesWithNonExistantUsers(self):
		toRemove = []
		for EID in self.entities:
			entity = self.entities[EID]
			owner = entity.getOwner()
			controller = entity.getController()
			if (not owner in self.GameState.contents['U']) or (not controller in self.GameState.contents['U']):
				toRemove.append(EID)
		for EID in toRemove:
			self.removeEntity(EID)




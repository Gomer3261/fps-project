### GameState Component ###

class Class:
	def __init__(self, slab):
		import RequestHandler
		self.RequestHandler = RequestHandler.Class()
	
		self.resetContents()
		self.changes = []
		
		self.EID = 1 # Entity ID
		
		print("GameState is ready.")
	
	
	
	def run(self, Admin, Networking):
		"""
		When we are the server, we send out full distributions of the gamestate periodically,
		but we also send out GameState Changes every tick.
		"""
		self.Admin = Admin
		self.RequestHandler.run(self, Networking.gpsnet) # Interprets requests from Networking...
		self.changes = [] # XXX Clearing Changes... (We don't need em for now!)
		# Distribution stuff goes here...
	
	
	### ================================================
	### Public Methods?
	### ================================================
	
	def reset(self):
		"""
		Resets the GameState, and also clears the GameState changes.
		"""
		self.resetContents()
		self.changes = []
	
	def applyNewContents(self, new):
		"""
		Totally clears the old GameState, and replaces it with a new edition of the GameState Contents.
		Clears the changes.
		"""
		self.contents = new
		self.changes = []

	def addEntity(self, type, owner=0, controller=0, args=[]):
		print("GameState.addEntity, type=%s"%(type))
		E = {}
		# Type (player, bot, vehicle, dob)
		E["T"] = type
		E["O"] = owner # OWNER UID
		E["C"] = controller # CONTROLLER UID
		
		E["OD"] = {'ARGS':args} # Owned Data (Initially includes ARGS)
		E["CD"] = {} # Controlled Data
		
		EID = self.generateEID()
		self.contents["E"][EID] = E
		return EID
	
	def removeEntity(self, EID):
		del self.contents['E'][EID]
		print("Entity (%s) removed."%(EID))
	
	def addUser(self, UID):
		U = {}
		U["N"] = "-NameError-"
		U["K"] = 0
		U["D"] = 0
		self.contents["U"][UID] = U
		return UID
	
	
	def getEntity(self, EID):
		return self.contents['E'][EID]
	
	
	
	### ================================================
	### Public Convenient Methods
	### ================================================
	
	def getEIDsByType(self, desiredType):
		EIDs = []
		for EID in self.contents['E']:
			type = self.contents['E'][EID]['T']
			if desiredType == type:
				EIDs.append(EID)
		return EIDs
	
	def getExplorer(self):
		explorers = self.getEIDsByType("explorer")
		if explorers:
			if len(explorers) > 1: print("CreepyError: There is more then one explorer entity in the GameState. Just thought you should know.")
			explorerEID = explorers[0]
			return explorerEID
		else:
			return None # No explorer :/
	
	def entityCount(self, name):
		"""
		Counts the number of *name* entities in the GameState.
		"""
		ents = self.getEIDsByType(name)
		if ents:
			return len(ents)
		else:
			return 0
	
	def countPlayers(self):
		"""
		Counts the number of 'player' entities in the GameState.
		"""
		players = self.getEIDsByType("player")
		if players:
			return len(players)
		else:
			return 0
	
	
	### ================================================
	### Private Methods
	### ================================================
	
	def resetContents(self):
		"""
		Resets the contents of the GameState...
		"""
		### GameState Contents ###
		self.contents = {}
		# Users (stored by Networking ticket)
		self.contents["U"] = {}
		# Entities (stored by Entity ID)
		self.contents["E"] = {}
	
	def generateEID(self):
		"""
		Generates a new unique Entity ID and returns it.
		"""
		chosen = self.EID
		self.EID += 1
		return chosen


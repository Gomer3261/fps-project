### GameState Component ###

class Class:
	def __init__(self, slab):
		import RequestHandler
		self.RequestHandler = RequestHandler.Class()
		
		self.reset()
		
		# Deprecated?
		self.nextEID = 1 # Entity ID
		self.nextUID = 1 # User ID
		
		
		print("GameState is ready.")
	
	
	
	def run(self, Admin, Network):
		self.Admin = Admin
		if Admin.weAreHost(): self.removeEntitiesWithNonExistantUsers()
		self.RequestHandler.run(self, Network) # Interprets requests from Network...
	
	
	### ================================================
	### Public Methods
	### ================================================
	
	def getUserName(self, UID):
		try:
			return self.contents['U'][UID]['N']
		except:
			return "-ErrorGettingUserName-"
	
	# Remove entities with non-existant users as controller/owner
	def removeEntitiesWithNonExistantUsers(self):
		toRemove = []
		for EID in self.contents['E']:
			entity = self.contents['E'][EID]
			owner = entity['O']
			controller = entity['C']
			if (not owner in self.contents['U']) or (not controller in self.contents['U']):
				toRemove.append(EID)
		for EID in toRemove:
			self.removeEntity(EID)
	
	def declareHost(self, UID):
		self.contents['owner'] = UID
		self.contents['controller'] = UID
		print("GS: %s has been declared the host of this game."%UID)
	
	def reset(self):
		"""
		Resets the GameState, and also clears the GameState changes.
		"""
		self.resetContents()
		#self.changes = []
	
	def applyNewContents(self, new):
		"""
		Totally clears the old GameState, and replaces it with a new edition of the GameState Contents.
		Clears the changes.
		"""
		self.contents = new
		#self.changes = []

	def addEntity(self, type, ownerUID=0, controllerUID=0, args=[]):
		print("GameState.addEntity, type=%s"%(type))
		E = {}
		# Type (player, bot, vehicle, dob)
		E["T"] = type
		E["O"] = ownerUID # OWNER UID
		E["C"] = controllerUID # CONTROLLER UID
		
		E["OD"] = {'ARGS':args} # Owned Data (Initially includes ARGS)
		E["CD"] = {} # Controlled Data
		
		EID = self.grabEID()
		self.contents["E"][EID] = E
		return EID
	
	def removeEntity(self, EID):
		del self.contents['E'][EID]
		print("GS: Entity (%s) removed."%(EID))
	
	def addUser(self, ticket, name="-NameError-"):
		UID = self.grabUID()
		print("GS: New User: %s, for ticket %s. Name=%s"%(UID, ticket, name))
		U = {}
		U["T"] = ticket # Network Ticket
		U["N"] = name
		U["K"] = 0
		U["D"] = 0
		self.contents["U"][UID] = U
		return UID
	
	def removeUser(self, UID):
		del self.contents['U'][UID]
		print("GS: User (%s) Removed."%UID)
	
	
	def getEntity(self, EID):
		return self.contents['E'][EID]
	
	
	
	### ================================================
	### Public Convenient Methods
	### ================================================
	def getDirectorEID(self):
		for EID in self.contents['E']:
			entityData=self.contents['E'][EID]; type=entityData['T']
			if type == 'director': return EID
		return None
	
	def getHost(self):
		host = self.contents['owner']
		return host
	
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
		
		# Owner and controller: not sure what the controller does, but the host
		# should be both of these.
		self.contents['owner'] = 0
		self.contents['controller'] = 0
		
		# ID Numbers...
		self.contents['IDN'] = {}
		self.contents['IDN']['EID'] = 1
		self.contents['IDN']['UID'] = 1
		
		# Users, stored by UID.
		self.contents["U"] = {}
		# Entities (stored by Entity ID)
		self.contents["E"] = {}
	
	def grabEID(self):
		"""
		Grabs the next EID
		"""
		chosen = self.contents['IDN']['EID']
		self.contents['IDN']['EID'] += 1
		return chosen
	
	def grabUID(self):
		"""
		Grabs the next UID
		"""
		chosen = self.contents['IDN']['UID']
		self.contents['IDN']['UID'] += 1
		return chosen

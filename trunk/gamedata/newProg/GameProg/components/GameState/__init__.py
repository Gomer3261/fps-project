### GameState Component ###

class Class:
	def __init__(self):
		import RequestHandler
		self.RequestHandler = RequestHandler.Class(self)
	
		self.resetContents()
		self.changes = []
		
		self.mode = "real" # Necessary?
		self.EID = 1 # Entity ID
	
	
	
	def run(self, Networking):
		"""
		When we are the server, we send out full distributions of the gamestate periodically,
		but we also send out GameState Changes every tick.
		"""
		self.RequestHandler.run(GameState, Networking.gpsnet) # Interprets requests from Networking...
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
	
	def applyFullDistro(self, new):
		"""
		Totally clears the old GameState, and replaces it with a new edition of the GameState Contents.
		Clears the changes.
		"""
		self.contents = new
		self.changes = []

	def addEntityDirectly(self, type):
		E = {}
		# Type (player, bot, vehicle, dob)
		E["T"] = type
		E["O"] = 0 # OWNER UID
		E["C"] = 0 # CONTROLLER UID
		
		E["OD"] = {} # Owned Data
		E["CD"] = {} # Controlled Data
		
		EID = self.generateEID()
		self.contents["E"][EID] = E
		return EID
	
	def addUserDirectly(self, UID):
		U = {}
		U["name"] = "-NameError-"
		U["kills"] = 0
		U["deaths"] = 0
		self.contents["U"][UID] = U
		return UID
	
	
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

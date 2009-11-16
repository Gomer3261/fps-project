### GameState Component ###

class Class:
	def __init__(self, cont=None):
		self.resetContents()
		self.changes = []
		
		self.mode = "real"
		self.EID = 1 # Entity ID
		self.TID = 1 # Trigger ID
	
	def resetContents(self):
		### GameState Contents ###
		self.contents = {}
		# Users (stored by Networking ticket)
		self.contents["U"] = {}
		# Entities (stored by Entity ID)
		self.contents["E"] = {}
		# Triggers (stored by Trigger ID)
		self.contents["T"] = {}
		# GameInformation
		self.contents["G"] = {}
		self.contents["G"]["S"] = "G" # GameInformation:State (L=Lobby, G=Game, I=Intermission)
		self.contents["G"]["GT"] = "dm" # GameInformation:GameType
		self.contents["G"]["L"] = "" # GameInformation:Level
	
	def reset(self):
		self.resetContents()
		self.changes = []
	
	def applyFullDistro(self, new):
		self.contents = new
		self.changes = []
	
	def getEID(self):
		chosen = self.EID
		self.EID += 1
		return chosen
	
	def getTID(self):
		chosen = self.TID
		self.TID += 1
		return chosen
	
	
	def addEntityDirectly(self, type):
		E = {}
		# Type (player, bot, vehicle, dob)
		E = ["T"] = type
		# Entity Controlled Attributes
		E["D"] = {}
		
		if type=='player':
			E['D']['A'] = {} # Player-Controlled Attributes
			E['D']['S'] = {} # Server-Controlled Attributes
		
		EID = self.getEID()
		self.contents["E"][EID] = E
		
		return EID
	
	def addUserDirectly(self, type):
		E = {}
		# Type (player, bot, vehicle, dob)
		E = ["T"] = type
		# Entity Controlled Attributes
		E["D"] = {}
		
		if type=='player':
			E['D']['A'] = {} # Player-Controlled Attributes
			E['D']['S'] = {} # Server-Controlled Attributes
		
		EID = self.getEID()
		self.contents["E"][EID] = E
		
		return EID

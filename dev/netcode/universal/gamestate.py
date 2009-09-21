#####################################
###### ----------------------- ######
###### ------ GAMESTATE ------ ######
###### ----------------------- ######
#####################################


class GAMESTATE:
	version = 4

	contents = {}

	changes = []

	def __init__(self):
		
		# U = Users
		# P = Players
		# B = Bots
		# OB = Objects
		# T = Triggers
		# V = Vehicles
		# G = Game Information (round state, etc.)
		
		# Users are kept by ticket, not username.
		self.contents["U"] = {}

		# Players are kept by ticket, not username.
		self.contents["P"] = {}

		
		self.contents["B"] = {}

		
		self.contents["OB"] = {}

		
		self.contents["T"] = {}

		
		self.contents["V"] = {}

		
		self.contents["G"] = {}
		# S = State (L=Lobby, G=Game)
		self.contents["G"]["S"] = "G"






	### ========================================================================
	### === Major Functions
	### ========================================================================

	def restart(self):
		self.contents = {}
		self.__init__()

	def applyFulldistro(self, new):
		self.contents = new
	
	def addUser(self, ticket, name="-NameError-"):
		U = {}
		
		# Name
		U["N"] = name
		
		# Stats
		U["S"] = {}
		U["S"]["S"] = 0 # Status
		U["S"]["K"] = 0 # Kills
		U["S"]["D"] = 0 # Deaths
		
		
	def addPlayer(self, ticket, name="-NameError-"):
		P = {}

		# Name
		P["N"] = name
		
		# Attributes
		P["A"] = {}
		P["A"]["P"] = [0.0, 0.0, 0.0]
		P["A"]["O"] = 0

		# Server-controlled Attributes
		P["SA"] = {}
		P["SA"]["L"] = 0 # Life Status
		P["SA"]["HP"] = 100 # Health Integer
		
		self.contents["P"][ticket] = P





	### ========================================================================
	### === Changes Functions
	### ========================================================================

	# Need to develop a system that avoids redundant changes in the changes list.
	# In other words, what if the player changes their position 4 times?
	# That will make the changes include all 4 of those position changes, when
	# really all that is needed is the latest one.

	def getChanges(self):
		changes = self.changes
		self.changes = []
		return changes

	def clearChanges(self):
		self.changes = []

	def applyChanges(self, changes):
		oldChanges = self.changes
		
		for change in changes:
			flag = change[0]
			info = change[1]

			if flag.lower() == "upc":
				ticket = info[0]
				A = info[1]
				B = info[2]
				data = info[3]
				self.upc(ticket, A, B, data)

			if flag.lower() == "upa":
				ticket = info[0]
				data = info[1]
				self.upa(ticket, data)

			if flag.lower() == "ar":
				ticket = info[0]
				request = info[1]
				data = info[2]
				self.ar(ticket, request, data)

		# Revert back to old changes
		self.changes = oldChanges

	#updatePlayerCustom: Allows the player to update a single attribute
	def upc(self, ticket, A, data):
		# ticket: The player's ID.
		# A: The variable name of the data.
		# data: The new data itself.
		import traceback
		try:
			self.contents["P"][ticket]["A"][A] = data
			self.changes.append( ("upc", [ticket, A, data]) )
		except:
			#print "Normal error with a Gamestate change (upc)"
			pass

	#updatePlayerAttributes
	def upa(self, ticket, data):
		# ticket: The player's ID.
		# data: The new attribute data.
		import traceback
		try:
			self.contents["P"][ticket]["A"] = data
			self.changes.append( ("upa", [ticket, data]) )
		except:
			#print "Normal error with a Gamestate change (upa)"
			pass

	# Action Request
	def ar(self, ticket, request, data):
		import traceback
		try:

			if request.lower() == "spawn":
				self.contents["P"][ticket]["SA"]["HP"] = 100
				self.contents["P"][ticket]["SA"]["L"] = 1
				self.changes.append( ("ar", [ticket, "spawn", 1]) )

			if request.lower() == "suicide":
				self.contents["P"][ticket]["SA"]["HP"] = 0
				self.contents["P"][ticket]["SA"]["L"] = 0
				self.changes.append( ("ar", [ticket, "suicide", 1]) )

		except:
			traceback.print_exc()
			pass




	

	### ========================================================================
	### === Informational Functions
	### ========================================================================

	def getPlayerNameList(self):
		names = []
		for ticket in self.contents["P"]:
			player = self.contents["P"][ticket]
			name = player["N"]
			names.append(name)
		return names

	def playerIsInGame(self, ticket):
		if ticket in self.contents["P"]:
			return 1 # Player is in game
		else:
			return 0 # Player is not in game

	def playerNameIsInGame(self, name):
		names = self.getPlayerNameList()
		if name in names:
			return 1
		else:
			return 0

	def getPlayerName(self, ticket):
		try:
			name = self.contents["P"][ticket]["N"]
			return name
		except:
			return "-NameError-"

	def playerIsAlive(self, ticket):
		try:
			life = self.contents["P"][ticket]["SA"]["L"]
			return life
		except:
			pass

	def getPlayerHP(self, ticket):
		try:
			HP = self.contents["P"][ticket]["SA"]["HP"]
			return HP
		except:
			pass

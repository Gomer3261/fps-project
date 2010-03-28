### Admin Component ###

class Class:
	def __init__(self, slab):
		"""
		### Admin Info ###
		# Contains all the information for setting up the game.
		self.AdminInfo = {}
		self.AdminInfo["host"] = 1 # 1=We are GameState host (online or server). 0=We are not GameState host (online)
		
		# must contain the information needed to create the Director.
		self.AdminInfo["director"] = {}
		self.AdminInfo["director"]["playlist"] = [] # A playlist of game settings.
		self.AdminInfo["director"]["index"] = 0 # current spot in the playlist.
		self.AdminInfo["director"]["intermission"] = None # None=In Game, float=intermission (time left).
		"""
		self.slab = slab
		self.gameInitiated = False
		self.UID = 0 # We don't have a UID!
		print("Admin's good.")
	
	
	def getGameInfo(self):
		import GameLogic
		return GameLogic.globalDict['gameInfo']
	
	def weAreHost(self):
		GI = self.getGameInfo()
		return GI['host']
	
	def getHostUID(self):
		if self.weAreHost():
			return self.UID
		else:
			if self.slab.Network.GPC: return self.slab.Network.GPC.hostUID
		return 0
	
	
	
	
	
	def initiationLoop(self, GameLogic, Network, GameState, Interface):
		"""
		Gets initiation information from the menus (via GameLogic.globalDict)
		and sets up the game with it.
		
		First, it sets up the game by determining the host and server values,
		and using them to decide if it needs to create the Director entity and
		start running the gameplayServer.
		
		We only need to add the director to the game when we are the game host, 
		because clients will replicate it.
		
		Secondly, it recovers networking sessions that have been saved.
		"""
		# Initiating the game when we haven't done that already.
		if not self.gameInitiated:
			self.gameInitiated = True
			
			print("\n=======================================================================================")
			print("====== Component Initiation Completed; Administrated Game Initiation starts now! ======")
			print("=======================================================================================\n")
			
			### Clearing the GameState ###
			GameState.reset()
			
			# GameInfo was found saved to the globalDict
			if "gameInfo" in GameLogic.globalDict:
				gameInfo = GameLogic.globalDict["gameInfo"]
				
				### ================================================
				### Setting up the Game
				### ================================================
				
				if gameInfo['host']:
					# First, we must obtain a UID, then declare that UID the owner and
					# controller of the GameState.
					username = gameInfo['username']
					UID = GameState.addUser(0, username) # Adding a user with no ticket signifies that the user is local.
					GameState.declareHost(UID)
					self.UID = UID
					
					# If we're the host, then we've got to create
					# the director entity.
					print("We're the host, creating the Director...")
					#GameState.createDirector(gameInfo["directorInfo"])
					item = ('GS', ('AR', ('SE', ('director', (self.UID, self.UID), [])) ))
					Network.send(item)
					print("Spawn director request sent via Network.send(item)...")
				
					if gameInfo["server"]:
						# We're a server!
						#Network.gpsnet.startServer(gameInfo["serverInfo"])
						address = gameInfo['hostaddress']
						print("\nAdmin, Starting Server...")
						Network.startServer(address, Interface)
						print("")
						Interface.out(" ", note=False)
				
				else: # We are not the host
					address = gameInfo['address']
					print("Admin, connecting as client...")
					Network.startClient(address)
				
				
				### ================================================
				### Network Session Recovery
				### ================================================
				
				#if "ms_session" in gameInfo:
				#	print("Recovering ms_session...")
				#	Network.msnet.recover(gameInfo["ms_session"])
				
				#if "gps_session" in gameInfo and (not gameInfo["host"]):
				#	print("Recovering gps_session...")
				#	Network.gpsnet.recover(gameInfo["gps_session"])
			
			print("\n===========================================================================")
			print("====== Administrated Game Initiation Complete; Game loop starts now! ======")
			print("===========================================================================\n")
			

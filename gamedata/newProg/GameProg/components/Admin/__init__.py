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
		self.gameInitiated = False
		self.UID = -1
		print("Admin's good.")
	
	
	def getUID(self):
		return self.UID
	
	
	def userControlLoop(self, Interface, GameState, Networking):
		"""
		DEPRECATED!!!
		"""
		if not Interface.Terminal.active:
			entityToSpawn = "nanoshooter"
			spawnStatus = Interface.Inputs.Controller.getStatus("spawn")
			if (spawnStatus == 1) and (not GameState.entityCount(entityToSpawn)):
				# Spawn the Player.
				package = ['GS', ['AR', ['SE', entityToSpawn]]]
				Networking.gpsnet.send(package)
				print("Spawn Entity request sent via Networking.gpsnet.send(request)...")
	
	
	
	
	
	def initiationLoop(self, GameLogic, Networking, GameState, Interface):
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
			
			
			# GameInfo was found saved to the globalDict
			if "gameInfo" in GameLogic.globalDict:
				gameInfo = GameLogic.globalDict["gameInfo"]
				
				### ================================================
				### Setting up the Game
				### ================================================
				
				if gameInfo['host']:
					# If we're the host, then we've got to create
					# the director entity.
					print("We're the host, creating the Director...")
					#GameState.createDirector(gameInfo["directorInfo"])
					package = ('GS', ('AR', ('SE', ('director', (self.UID, self.UID), [])) ))
					Networking.gpsnet.send(package)
					print("Spawn director request sent via Networking.gpsnet.send(request)...")
				
				if gameInfo["host"] and gameInfo["server"]:
					# We're a server!
					#Networking.gpsnet.startServer(gameInfo["serverInfo"])
					address = gameInfo['address']
					Networking.gpsnet.startServer(address)
					Networking.gpsnet.startClient(address)
					Interface.out(" ", note=False)
				
				
				### ================================================
				### Networking Session Recovery
				### ================================================
				
				#if "ms_session" in gameInfo:
				#	print("Recovering ms_session...")
				#	Networking.msnet.recover(gameInfo["ms_session"])
				
				#if "gps_session" in gameInfo and (not gameInfo["host"]):
				#	print("Recovering gps_session...")
				#	Networking.gpsnet.recover(gameInfo["gps_session"])
			
			print("\n===========================================================================")
			print("====== Administrated Game Initiation Complete; Game loop starts now! ======")
			print("===========================================================================\n")
			Interface.out("Welcome!")
			Interface.out("You can press ~ (tilde) to toggle the in-game terminal.")
			Interface.out("You can press spacebar to spawn a testing entity (yes you can spawn multiple, that's not a glitch).")
			Interface.out("Use WASD keys and mouse movement to control the nanoshooter testing entity.")
			Interface.out("Press the delete key to kill the testing entity.")
			Interface.out("If those controls don't work, you should enter /defaultOptions() into the terminal. The terminal can also be used to customize any of your controls.")
			Interface.out("That's all for now folks.")
			Interface.out(" ", note=False)
			

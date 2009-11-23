### Admin Component ###

class Class:
	def __init__(self):
		self.gameInitiated = False
		
		### Admin Info ###
		# Contains all the information for setting up the game.
		self.AdminInfo = {}
		self.AdminInfo["host"] = 1 # 1=We are GameState host (online or server). 0=We are not GameState host (online)
		
		# must contain the information needed to create the Director.
		self.AdminInfo["director"] = {}
		self.AdminInfo["director"]["playlist"] = [] # A playlist of game settings.
		self.AdminInfo["director"]["index"] = 0 # current spot in the playlist.
		self.AdminInfo["director"]["intermission"] = None # None=In Game, float=intermission (time left).
	
	
	
	
	def run(self, GameLogic, Networking, GameState):
		"""
		Gets initiation information from the menus (via GameLogic.globalDict)
		and sets up the game with it.
		
		First, it sets up the game by determining the host and server values,
		and using them to decide if it needs to create the Director entity and
		start running the gameplayServer.
		
		Secondly, it recovers networking sessions that have been saved.
		"""
	
		# Initiating the game when we haven't done that already.
		if not self.gameInitiated:
			
			# GameInfo was found saved to the globalDict
			if "gameInfo" in GameLogic.globalDict:
				gameInfo = GameLogic.globalDict["gameInfo"]
				
				### ================================================
				### Setting up the Game
				### ================================================
				
				if gameInfo["host"]:
					# If we're the host, then we've got to create
					# the director entity.
					GameState.createDirector(gameInfo["directorInfo"])
				
				if gameInfo["host"] and gameInfo["server"]:
					# We're a server!
					Networking.gpsnet.startServer(gameInfo["serverInfo"])
				
				
				### ================================================
				### Networking Session Recovery
				### ================================================
				
				if "ms_session" in gameInfo:
					print("Recovering ms_session...")
					Networking.msnet.recover(gameInfo["ms_session"])
				
				if "gps_session" in GameInfo and (not gameInfo["host"]):
					print("Recovering gps_session...")
					Networking.gpsnet.recover(gameInfo["gps_session"])
			
			self.gameInitiated = True

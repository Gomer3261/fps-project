"""
Stores the localgame, and replicates it based on the gamestate.
"""
INIT = 1

players = None


def run(con):
	import modules
	gamestate = modules.gamecontrol.gamestate.gamestate
	global players
	
	players.replicate(gamestate, con)
	players.run()


class PLAYERS:
	"""
	Stores and replicates players.
	"""
	storage = {} # Stores players by their users' tickets (each user gets a unique ticket when they join the game)
	
	def spawnPlayer(self, ticket, spawnObj, mode="real"):
		"""
		Creates a player handler and put it in storage.
		"""
		import modules
		players = modules.entities.players
		handler = players.PLAYER(ticket, spawnObj, mode)
		self.storage[ticket] = handler
	
	def deletePlayer(self, ticket):
		"""
		Deletes a player from storage.
		"""
		#handler = self.storage[ticket]
		#handler.terminate()
		del self.storage[ticket]
	
	def getPlayer(self, ticket):
		"""
		Gets a player handler
		"""
		try:
			handler = self.storage[ticket]
			return handler
		except:
			return None
	
	def getLocalPlayer(self):
		"""
		Get's the local player handler, if it exists.
		"""
		import modules
		info = modules.gamecontrol.info
		gamestate = modules.gamecontrol.gamestate.gamestate
		
		if info.inGame and info.ticket and gamestate.playerIsInGame(info.ticket):
			try:
				handler = self.getPlayer(info.ticket)
				return handler
			except:
				pass
		return None
	
	def run(self):
		for ticket in self.storage:
			player = self.storage[ticket]
			player.run()
	
	def replicate(self, gamestate, con):
		"""
		Replicates the players from the gamestate.
		If a player is in the gamestate but not in storage, a player is added.
		Each player handler is responsible for performing any further replication,
		including self-deletion.
		"""
		
		# During instantiation, handlers use the spawnObj to spawn gameObjects.
		spawnObj = con.owner
		
		import modules
		gamestate = modules.gamecontrol.gamestate.gamestate
		info = modules.gamecontrol.info
		localPlayerTicket = info.ticket
		
		
		
		### ======------ SPAWNING PLAYERS ------====== ###
		
		# Adding players to storage if they are not in the gamestate.
		for ticket in gamestate.contents["P"]:
			if ticket not in self.storage:
				# If it's us, the local player, then the handler mode will be "real"
				if ticket == localPlayerTicket:
					mode = "real"
				# If it's not us, it's another player, so we create the handler in "proxy" mode.
				else:
					mode = "proxy"
				# Now we actually spawn the player.
				self.spawnPlayer(ticket, spawnObj, mode)

players = PLAYERS()
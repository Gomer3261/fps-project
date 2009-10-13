"""
Stores the localgame, and replicates it based on the gamestate.
"""
INIT = 1

players = None


def run(con):
	import modules
	gamestate = modules.gamecontrol.gamestate.gamestate
	global players
	global explorers
	
	players.replicate(gamestate, con)
	explorers.replicate(con)
	players.run()
	explorers.run()


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
		
		terminal = modules.interface.terminal
		terminal.output("Player Spawned. Ticket: %s, mode: %s"%(ticket, mode))
	
	def deletePlayer(self, ticket):
		"""
		Deletes a player from storage.
		"""
		#handler = self.storage[ticket]
		#handler.terminate()
		del self.storage[ticket]
		import modules
		terminal = modules.interface.terminal
		terminal.output("Player Deleted. Ticket: %s"%(ticket))
	
	def killAllPlayers(self):
		"""
		===DEPRECATED===
		Kills and delete all players
		( The new way to do it is to remove them from the gamestate instead)
		"""
		for ticket in self.storage:
			player = self.storage[ticket]
			player.alive = 0
	
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
		try:
			for ticket in self.storage:
				player = self.storage[ticket]
				player.run()
				#print "Running: %s"%(ticket)
		except:
			# Dictionary changed size during iteration...
			#import traceback
			#traceback.print_exc()
			pass
	
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
				
				
				
				
				
				
				
				
class EXPLORERS:
	"""
	Stores the explorer object.
	"""
	
	explorer = None
	
	spawnRequest = 0
	
	def spawnExplorer(self, spawnObj):
		"""
		Creates an explorer handler and saves it.
		"""
		
		import modules
		explorer = modules.entities.explorer
		handler = explorer.EXPLORER(spawnObj)
		self.explorer = handler
		
		#terminal = modules.interface.terminal
		#terminal.output("Explorer Spawned.")

	
	def run(self):
		try: 
			
			if self.explorer:
				self.explorer.run()

		
		except:
			# Dictionary changed size during iteration...
			import traceback
			traceback.print_exc()
			pass
	
	def replicate(self, con):
		"""
		This method should not exist.
		"Replication" is the process of modifying the local game world to 
		represent that which is described by the gamestate.
		
		What is seen here, is the action of spawning explorer objects, 
		which has nothing to do with replication.
		"""
		#spawnObj = con.owner
		#if self.spawnRequest and not self.explorer:
		#	self.spawnExplorer(spawnObj)
		#	self.spawnRequest = 0
		pass
			

	

players = PLAYERS()
explorers = EXPLORERS()
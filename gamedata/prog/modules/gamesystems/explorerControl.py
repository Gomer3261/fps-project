### EXPLORER SYSTEM ###

# It's pretty simple really.
# Basically, this script just keeps an explorer around when the player is dead.
# It deletes the explorer when the player is alive.


def run(con):
	import modules
	localgame = modules.gamecontrol.localgame
	player = localgame.players.getLocalPlayer()
	
	
	
	activePlayer = 0
	if player:
		if player.alive:
			activePlayer = 1
	
	
	
	if not activePlayer:
		# Assert that an explorer is active
		if not localgame.explorers.explorer:
			localgame.explorers.spawnExplorer(con.owner)
	
	else:
		# Kill the explorer.
		if localgame.explorers.explorer:
			localgame.explorers.explorer.alive = 0

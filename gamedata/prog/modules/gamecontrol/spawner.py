### The Spawner ###
"""
Simple and temporary system for player-controlled spawning and suicide.
"""

import modules

def run(con):
	director = modules.gamecontrol.director
	inputs = modules.interface.inputs
	terminal = modules.interface.terminal
	
	gamestate = modules.gamecontrol.gamestate.gamestate
	info = modules.gamecontrol.info
	
	spawn = inputs.controller.getStatus("spawn")
	suicide = inputs.controller.getStatus("suicide")

	if (not terminal.active) and info.ticket and gamestate.userIsInGame(info.ticket):
		if spawn == 1 and (not gamestate.playerIsInGame(info.ticket)):
			print "Requesting Spawn"
			requestSpawn()

		if suicide == 1 and gamestate.playerIsInGame(info.ticket):
			print "Requesting Suicide"
			requestSuicide()



def requestSpawn():
	director = modules.gamecontrol.director
	info = modules.gamecontrol.info
	director.router.send( ("ar", [info.ticket, "spawn", 1]) )

def requestSuicide():
	director = modules.gamecontrol.director
	info = modules.gamecontrol.info
	director.router.send( ("ar", [info.ticket, "suicide", 1]) )

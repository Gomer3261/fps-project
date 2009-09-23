import modules
from modules import *

def gs():
	terminal = modules.interface.terminal
	gamestate = modules.gamecontrol.gamestate.gamestate
	terminal.output( str(gamestate.contents) )

def printUsers():
	terminal = modules.interface.terminal
	gamestate = modules.gamecontrol.gamestate.gamestate
	for ticket in gamestate.contents["U"]:
		name = gamestate.contents["U"][ticket]["N"]
		terminal.output( str(name) )

def printPlayers():
	terminal = modules.interface.terminal
	gamestate = modules.gamecontrol.gamestate.gamestate
	for ticket in gamestate.contents["P"]:
		name = gamestate.contents["P"][ticket]["N"]
		terminal.output( str(name) )
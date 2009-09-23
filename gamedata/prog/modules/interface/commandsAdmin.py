import modules
from modules import *

def gs():
	terminal = modules.interface.terminal
	gamestate = modules.gamecontrol.gamestate.gamestate
	terminal.output( str(gamestate.contents) )

def users():
	terminal = modules.interface.terminal
	gamestate = modules.gamecontrol.gamestate.gamestate
	for ticket in gamestate.contents["U"]:
		name = gamestate.contents["U"][ticket]["N"]
		terminal.output( str(name) )

def players():
	terminal = modules.interface.terminal
	gamestate = modules.gamecontrol.gamestate.gamestate
	for ticket in gamestate.contents["P"]:
		name = gamestate.contents["P"][ticket]["N"]
		terminal.output( str(name) )

def playerDetails():
	terminal = modules.interface.terminal
	gamestate = modules.gamecontrol.gamestate.gamestate
	
	#terminal.output( "\n\n" )
	
	for ticket in gamestate.contents["P"]:
		player = gamestate.contents["P"][ticket]
		name = player["N"]
		terminal.output( str(name) )
		
		for attrName in player["A"]:
			terminal.output( "  - %s: %s"%(attrName, str(player["A"][attrName])))

def info():
	terminal = modules.interface.terminal
	info = modules.gamecontrol.info
	terminal.output("   %s: %s"%("mode", str(info.mode)))
	terminal.output("   %s: %s"%("inGame", str(info.inGame)))
	terminal.output("   %s: %s"%("ticket", str(info.ticket)))
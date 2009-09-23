import modules
from modules import *

def gs():
	terminal = modules.interface.terminal
	gamestate = modules.gamecontrol.gamestate.gamestate
	terminal.output( str(gamestate.contents) )

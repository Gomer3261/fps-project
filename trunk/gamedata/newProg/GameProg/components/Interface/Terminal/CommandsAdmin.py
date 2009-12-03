
class Class():
	def __init__(self, slab):
		self.slab = slab

#	def localPlayer():
#		localPlayer = gamecontrol.localgame.players.getLocalPlayer()
#		return localPlayer
#
#	def gs():
#		"""
#		Outputs the current gamestate information to the terminal.
#		"""
#		terminal = modules.interface.terminal
#		gamestate = modules.gamecontrol.gamestate.gamestate
#		terminal.output( str(gamestate.contents) )
#
#	def users():
#		"""
#		Outputs a list of users in the gamestate, to the terminal.
#		"""
#		terminal = modules.interface.terminal
#		gamestate = modules.gamecontrol.gamestate.gamestate
#		for ticket in gamestate.contents["U"]:
#			name = gamestate.contents["U"][ticket]["N"]
#			terminal.output( "%s: %s"%(str(name), ticket) )
#
#	def players():
#		"""
#		Outputs a list of players in the gamestate, to the terminal.
#		"""
#		terminal = modules.interface.terminal
#		gamestate = modules.gamecontrol.gamestate.gamestate
#		for ticket in gamestate.contents["P"]:
#			name = gamestate.contents["P"][ticket]["N"]
#			terminal.output( "%s: %s"%(str(name), ticket) )
#
#	def playerDetails():
#		"""
#		Ouputs more player details to the terminal.
#		"""
#		terminal = modules.interface.terminal
#		gamestate = modules.gamecontrol.gamestate.gamestate
#		localgame = modules.gamecontrol.localgame
#		
#		#terminal.output( "\n\n" )
#		
#		for ticket in gamestate.contents["P"]:
#			player = gamestate.contents["P"][ticket]
#			name = player["N"]
#			terminal.output( "%s, %s, %s"%(str(name), ticket, localgame.players.getPlayer(ticket).mode) )
#			
#			for infopack in player:
#				if hasattr(player[infopack], "keys"):
#					terminal.output("   %s:"%(infopack))
#					for attrName in player[infopack]:
#						terminal.output( "      - %s: %s"%(attrName, str(player[infopack][attrName])))
#				else:
#					terminal.output("   %s: %s"%(infopack, player[infopack]))
#
#	def info():
#		"""
#		Outputs some basic gamecontrol information to the terminal.
#		"""
#		terminal = modules.interface.terminal
#		info = modules.gamecontrol.info
#		terminal.output("   %s: %s"%("mode", str(info.mode)))
#		terminal.output("   %s: %s"%("inGame", str(info.inGame)))
#		terminal.output("   %s: %s"%("ticket", str(info.ticket)))
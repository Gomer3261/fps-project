### The Master Script ###
"""
The highest level of programming; it's responsible for running the entire game.
"""
def initiate(cont):
	import slab
	if not slab.INIT:
		import components
	
		### Admin ###
		if not hasattr(slab, "Admin"): slab.Admin = components.Admin.Class(slab)
		
		### GameState ###
		if not hasattr(slab, "GameState"): slab.GameState = components.GameState.Class(slab)
		
		### LocalGame ###
		if not hasattr(slab, "LocalGame"): slab.LocalGame = components.LocalGame.Class(slab)
		
		### Gui ###
		if not hasattr(slab, "Gui"): slab.Gui = components.Gui.Class(slab)
		
		### Interface ###
		if not hasattr(slab, "Interface"): slab.Interface = components.Interface.Class(slab)
		
		### Network ###
		if not hasattr(slab, "Network"): slab.Network = components.Network.Class(slab)
		
		### Resources ###
		if not hasattr(slab, "Resources"): slab.Resources = components.Resources.Class(slab)
		
		# Initiating Game Information #
		import GameLogic
		
		GI = {}
		
		GI['host'] = False
		GI['server'] = False
		
		address = "chasemoskal.dyndns.org"
		tcpPort, udpPort = 3204, 3204
		
		GI['address'] = slab.Network.comms.makeAddressString( (address, tcpPort, udpPort) )
		GI['hostaddress'] = slab.Network.comms.makeAddressString( (slab.Network.IP, tcpPort, udpPort) )
		
		username = slab.Interface.Options.getSetting("username")
		if username: GI['username'] = username
		else: GI['username'] = "-NoName-"
		
		GameLogic.globalDict['gameInfo'] = GI
		
		###
		### INIT Completed.
		slab.INIT = 1
		###
		




def run(cont):
	try:
		import GameLogic
		
		### ================================================
		### Initiations
		### ================================================
		initiate(cont) # Only actually initiates the first time...
		
		import slab
		Admin = slab.Admin
		GameState = slab.GameState
		Gui = slab.Gui
		Interface = slab.Interface
		LocalGame = slab.LocalGame
		Network = slab.Network
		Resources = slab.Resources
		
		
		### ================================================
		### The Game Loop
		### ================================================
		
		Admin.initiationLoop(GameLogic, Network, GameState, Interface) # Setting up the game
		
		Network.run(Admin, GameState, Interface) # Maintaining connections and stuff, and also receiving data to inBundles.
		
		Interface.run(Network, GameState) # Runs the interface (user inputs).
		GameState.run(Admin, Network) # Runs the GameState: represents the game world based on changes it finds in the Network in buffer.
		LocalGame.run(Admin, GameState, Network, Resources, Interface) # LocalGame: Reflects the scene described by GameData.
		
		#if Network.inBundles: print(Network.inBundles)
		Network.inBundles = [] # Clearing the inBundles buffer
		Network.outgoing(Admin, GameState, Interface) # Asynchronously sends out data that has accumulated in the buffers.
	
	
	
	
	
	
	
	
	except:
		import traceback
		tb = traceback.format_exc()
		print("\n\nMasterError: %s\n\n"%(tb))

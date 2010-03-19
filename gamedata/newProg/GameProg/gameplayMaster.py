### The Master Script ###
"""
The highest level of programming; it's responsible for running the entire game.
"""
def initiate(cont):
	import slab
	if not slab.INIT:
	
		### Admin ###
		from components import Admin
		if not hasattr(slab, "Admin"): slab.Admin = Admin.Class(slab)

		### GameGoodies ###
		from components import GameGoodies
		if not hasattr(slab, "GameGoodies"): slab.GameGoodies = GameGoodies.Class(slab)
		
		### GameState ###
		from components import GameState
		if not hasattr(slab, "GameState"): slab.GameState = GameState.Class(slab)
		
		### LocalGame ###
		from components import LocalGame
		if not hasattr(slab, "LocalGame"): slab.LocalGame = LocalGame.Class(slab)
		
		### Gui ###
		from components import Gui
		if not hasattr(slab, "Gui"): slab.Gui = Gui.Class(slab)
		
		### Interface ###
		from components import Interface
		if not hasattr(slab, "Interface"): slab.Interface = Interface.Class(slab)
		
		### Networking ###
		from components import Networking
		if not hasattr(slab, "Networking"): slab.Networking = Networking.Class(slab)
		
		### Resources ###
		from components import Resources
		if not hasattr(slab, "Resources"): slab.Resources = Resources.Class(slab)
		
		# Initiating Game Information #
		import GameLogic
		GI = {}
		GI['host'] = True
		GI['server'] = True
		GI['address'] = "chasemoskal.dyndns.org:3205"
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
		from slab import *
		
		
		### ================================================
		### The Game Loop
		### ================================================
		
		Admin.initiationLoop(GameLogic, Networking, GameState, Interface) # Setting up the game
		#Admin.userControlLoop(Interface, GameState, Networking) # DEPRECATED
		
		Networking.msnet.run(Admin, Interface) # Asynchronous operations with the Master Server.
		Networking.gpsnet.run(Admin, Interface) # Asynchronous operations with the Gameplay Server.
		Networking.gpsnet.incoming() # Receiving data to the in buffer.
		
		Interface.run() # Runs the interface (user inputs).
		GameState.run(Admin, Networking) # Runs the GameState: represents the game world based on changes it finds in the Networking in buffer.
		LocalGame.RequestHandler.run(LocalGame, Networking.gpsnet)
		LocalGame.run(Admin, GameState, Networking, Resources, Interface) # LocalGame: Reflects the scene described by GameData.
		GameGoodies.run() # Runs GameGoodies
		
		Networking.gpsnet.inItems = [] # XXX Temporary! -- what's temporary about this ?
		Networking.gpsnet.outgoing(Admin) # Asynchronously sends out data that has accumulated in the buffers.
	
	
	
	
	
	
	
	
	
	except:
		import traceback
		tb = traceback.format_exc()
		print("\n\nMasterError: %s\n\n"%(tb))

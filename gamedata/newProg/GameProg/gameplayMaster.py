### The Master Script ###
"""
The highest level of programming; it's responsible for running the entire game.
"""
def initiate(cont):
	import slab
	if not slab.INIT:

		### GameGoodies ###
		from components import GameGoodies
		if not hasattr(slab, "GameGoodies"): slab.GameGoodies = GameGoodies.Class(cont)
		
		### GameState ###
		from components import GameState
		if not hasattr(slab, "GameState"): slab.GameState = GameState.Class(cont)
		
		### LocalGame ###
		from components import LocalGame
		if not hasattr(slab, "LocalGame"): slab.LocalGame = LocalGame.Class(cont)
		
		### Gui ###
		from components import Gui
		if not hasattr(slab, "Gui"): slab.Gui = Gui.Class(cont)
		
		### Interface ###
		from components import Interface
		if not hasattr(slab, "Interface"): slab.Interface = Interface.Class(cont)
		
		### Networking ###
		from components import Networking
		if not hasattr(slab, "Networking"): slab.Networking = Networking.Class(cont)
		
		### Resources ###
		from components import Resources
		if not hasattr(slab, "Resources"): slab.Resources = Resources.Class(cont)
		
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
		### Networking Session Recovery
		### ================================================
		
		# Recovering master server session from 
		# the main menu via GameLogic.globalDict
		if MasterInfo.try_mscon:
			if not Networking.msnet.connected:
				if "ms_session" in GameLogic.globalDict:
					print("Reconnecting to MS.")
					ms_session = GameLogic.globalDict["ms_session"]
					del GameLogic.globalDict["ms_session"]
					Networking.msnet.reconnect(ms_session)
				else:
					print("No ms_session info found; not reconnecting to MS.")
			MasterInfo.try_mscon = 1
		
		# Connecting to GPS based on inherited information.
		if MasterInfo.try_gpscon:
			if not Networking.gpsnet.connected:
				if "gpscon" in GameLogic.globalDict:
					print("Connecting to GPS")
					gpscon = GameLogic.globalDict["gpscon"]
					del GameLogic.globalDict["gpscon"]
					Networking.gpsnet.reconnect(gpscon)
				else:
					print("No inherited gpscon info; not connecting to GPS.")
			MasterInfo.try_gpscon = 1
		
		
		
		
		
		
		
		### ================================================
		### The Game Loop
		### ================================================
		
		Networking.msnet.run(MasterInfo) # Asynchronous operations with the Master Server.
		Networking.gpsnet.run(MasterInfo) # Asynchronous operations with the  Gameplay Server.
		Networking.gpsnet.incoming() # Receiving data to the in buffer.
		
		Interface.run() # Runs the interface (user inputs).
		GameState.run(Networking) # Runs the GameState: represents the game world based on changes it finds in the Networking in buffer.
		LocalGame.run(Networking) # LocalGame: Reflects the scene described by GameData.
		GameGoodies.run() # Runs GameGoodies
		
		Networking.gpsnet.outgoing(LocalGame) # Asynchronously sends out data that has accumulated in the buffers.
	
	
	
	
	
	
	
	
	
	except:
		import traceback
		tb = traceback.format_exc()
		print("\n\nMasterError: %s\n\n"%(tb))

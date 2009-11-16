### The Master Script ###
"""
The highest level of programming; it's responsible for running the entire game.
"""

class Class:
	def __init__(self):
		pass
	
	def run(self):
		try:
			import GameLogic
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
					else:
						print("No inherited gpscon info; not connecting to GPS.")
				MasterInfo.try_gpscon = 1
			
			
			
			### ================================================
			### The Game Loop
			### ================================================
			
			Networking.msnet.run(MasterInfo)
			Networking.gpsnet.run(MasterInfo)
			Networking.gpsnet.handleIn()
			
			Interface.run()
			GameState.run()
			GameGoodies.run()
			
			Networking.gpsnet.handleOut()
		
		
		
		except:
			import traceback
			tb = traceback.format_exc()
			print("\n\nMasterError: %s\n\n"%(tb))

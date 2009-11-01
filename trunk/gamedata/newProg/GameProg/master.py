### The Master Script ###
"""
The highest level of programming; it's responsible for running the entire game.
"""

def run():
	try:
		from slab import *
		
		# Running each component of the game...
		Ai.run()
		Director.run()
		GameBase.run()
		GameState.run()
		Gui.run()
		Interface.run()
		LocalGame.run()
		Networking.run()
		# These two don't actually need to be run...
		Resources.run()
		Tools.run()
		
	except:
		import traceback
		tb = traceback.format_exc()
		print("\n\nError: %s\n\n"%(tb))

### ########################## ###
### ### ------ GUNS ------ ### ###
### ########################## ###
### # The FPS Project
INIT = 1

class GUN:
	"""
	A Gun Handler. 
	Contains a firearm object. It handles the operation of a firearm in the game, 
	including animations and timing and such. 
	"""
	import firearms
	firearm = firearms.FIREARM()
	
	def run(self, player):
		"""
		The player that is using this gun handler calls this run function.
		A reference to the player object is given so that the weapon can access things 
		that are related to the player (such as the inventory's ammopile).
		"""
		pass

# The Slab
"""
Module that will be used to store instances of GameProg components.
Also contains the master info class/object.
"""
INIT = 0

class MasterInfoClass:
	def __init__(self):
		
		# This remembers if we've tried to connect to the Master or Gameplay servers.
		# That way we don't end up constantly trying to connect.
		self.try_mscon = 0
		self.try_gpscon = 0

MasterInfo = MasterInfoClass()
# The Slab
"""
Module that will be used to store instances of GameProg components.
Also contains the master info class/object.
"""
INIT = 0

class MasterInfoClass:
	def __init__(self):
		self.try_mscon = 0
		self.try_gpscon = 0

MasterInfo = MasterInfoClass()
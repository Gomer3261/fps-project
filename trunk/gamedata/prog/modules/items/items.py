############################
### ------ items ------ ####
############################

# This module stores the base class for items

class ITEM:
	"""The base item class"""
	
	cost = 0
	weight = 0
	
class WEAPON(ITEM):
	"""The base weapon class - primary and secondary subclass this"""
	
	barrelLength = 0
	
class HELMET(ITEM):
	"""The helmet base class - the hud depends on the helmet worn"""
	
	scene = ""
	life = 0
	
class ARMOR(ITEM):
	"""The armor base class - armors can slow down bullets to reduce damage"""
	
	life = 0
	speedReduction = 0
	
class BELT(ITEM):
	"""The belt base class - grenade and med pack capacities depend on the belt"""
	
	grenadeMax = 0
	medpackMax = 0
	
class MED(ITEM):
	"""The med pack base class"""
	
	weight = 0
	
class GRENADE(ITEM):
	"""The grenade base class"""
	
	weight = 0
	
class AMMOPILE(ITEM):
	"""Keeps track of the number of bullets"""
	
	ptl = 0
	sta = 0
	dmr = 0
	amr = 0
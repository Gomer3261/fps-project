################################
### ------ inventory ------ ####
################################

class INVENTORY:
	"""
	Manages the player's possessions.
	
	Here's what's going down.
	Items are things that the player can equip and use.
	Ammo (found in the ammopile) can be used by items.
	For example, a gun item would use bullets from the ammopile.
	
	This is the part that may be confusing at first:
	Grenade items use grenades from the ammopile.
	A grenade item is not a grenade itself; the grenade item is what 
	is throwing the grenades (which come from the ammopile).
	
	The same thing goes for all items.
	A med item might consume meds (like syrettes or medkits) from the ammopile.
	"""
	
	activeItem = "primary" # The active item! For example, could be "primary", or "grenade".
	
	items = {}
	items["primary"] = None
	items["secondary"] = None
	items["sidearm"] = None
	items["grenade"] = None
	items["med"] = None
	
	# (Currently useless)
	armor = None
	helmet = None
	
	# Ammunition (includes bullets, grenades, meds)
	ammopile = None
	
	
	
	def __init__(self, player):
		import modules.items.data as data
		self.data = data
		# Initiating the Ammopile.
		self.ammopile = self.data.AMMOPILE(player)
		
		# Giving the player a basic gun.
		import modules.items as items
		self.items["primary"] = items.guns.GUN(player)
	
	
	
	def getActiveItem(self):
		"""
		Returns the handler object for the active item.
		"""
		return self.items[self.activeItem]
	
	def changeActiveItem(self, new="primary"):
		if new in self.items:
			self.activeItem = new
		else:
			raise Exception, "Could not make %s the active item; this inventory does not possess %s"%(new, new)

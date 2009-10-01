################################
### ------ inventory ------ ####
################################

class INVENTORY:
	"""Manages the player's items"""
	
	# Weapons
	primary = None
	secondary = None
	
	# Armor
	armor = None
	
	# Helmet
	helmet = None
	
	# Belt
	belt = None
	
	# Meds and grenades
	meds = []
	grenades = []
	
	# Ammo
	ammopile = None
	
	def __init__(self):
		import modules.items.data as data
		self.data = data
		# We need a starting belt
		self.belt = self.data.BELT()
		# And an ammopile
		self.ammopile = self.data.AMMOPILE()
	
	def changePrimary(self, weapon):
		self.primary = weapon
		
	def changeSecondary(self, weapon):
		self.secondary = weapon
		
	def changeArmor(self, armor):
		self.armor = armor
		
	def changeHelmet(self, helm):
		self.helmet = helm
		
	def changeBelt(self, belt):
		self.belt = belt
		
	def addMed(self, med):
		if self.belt.medpackMax < len(self.belt.meds):
			self.meds.append(med)
		else:
			# Pass for now, but we need to raise an error
			pass 
		
	def addGrenade(self, gren):
		if self.belt.grenadeMax < len(self.belt.grenades):
			self.grenades.append(gren)
		else:
			# Pass for now, but we need to raise an error
			pass


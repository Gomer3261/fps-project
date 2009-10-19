############################
### ------ items ------ ####
############################

class AMMOPILE:
	"""
	Keeps track of the amount of ammunition a player has.
	"""
	import modules.classes.bulletTypes as bulletTypes
	
	# Default bullet values
	bullets = {}
	bullets["PTL"] = 36
	bullets["STA"] = 150
	bullets["DMR"] = 80
	bullets["AMR"] = 20
	
	# Default grenade values
	grenades = {}
	grenades["frag"] = 2
	grenades["smoke"] = 1
	
	# Default med values
	meds = {}
	meds["syrette"] = 2
	meds["kit"] = 0
	
	
	
	player = None
	def __init__(self, player):
		self.player = player
	
	
	
	
	def getWeight(self):
		totalWeight = 0.0
		for ammoType in self.bullets:
			totalWeight += self.bulletTypes.bullets[ammoType].weight * self.bullets[ammoType]
		return totalWeight
	
	
	
	
	def addBullets(self, bulletType, quantity):
		"""
		Adds a quantity of ammunition to a given ammoType, 
		and returns the new quantity of ammunition.
		"""
		# If the ammo type is missing, then raise an error.
		if bulletType not in self.bullets:
			raise Exception, "Inventory Error: AmmoType %s not in ammopile."%(bulletType)
			
		self.bullets[bulletType] += quantity
		return self.bullets[bulletType]
	
	def takeBullets(self, bulletType, desiredQuantity):
		"""
		Takes ammo of specified bulletType from ammopile.
		Tries to take the full desired quantity; if there is not
		sufficient ammo in the pile to satisfy desiredQuanity, it takes
		all of the ammo available.
		"""
		
		# If the ammo type is missing, then raise an error.
		if bulletType not in self.bullets:
			raise Exception, "Inventory Error: AmmoType %s not in ammopile."%(bulletType)
		if self.bullets[bulletType] < 0:
			print "ERROR: Negative %s ammo quantity? wtf?"%(bulletType)
			self.bullets[bulletType] = 0
		
		obtainedAmmo = 0
		
		# If there is ammo of that type...
		if self.bullets[bulletType]:
			# If there is less ammo left than the magazine's capacity,
			# we fill the magazine up with all the ammo in the pile.
			if self.bullets[bulletType] < desiredQuantity:
				obtainedAmmo = self.bullets[bulletType]
				self.bullets[bulletType] = 0
			# If there is enough ammo in the pile, then we just take it. Easy.
			else:
				obtainedAmmo = desiredQuantity
				self.bullets[bulletType] -= desiredQuantity
		
		return obtainedAmmo
	
	
	
	def produceMagazine(self, bulletType, magazineCapacity):
		"""
		Returns a magazine (which is a list of bullet objects),
		filled with as many bullets possible, taken from the 
		ammopile with takeBullets().
		"""
		# Amount of ammunition obtained
		obtainedAmmo = self.takeBullets(bulletType, magazineCapacity)
		
		newMagazine = []
		# Makes an instance of BULLET for each bullet in obtainedAmmo.
		for i in range(obtainedAmmo):
			BULLET = self.bulletTypes.bullets[bulletType]
			bullet = BULLET()
			newMagazine.append(bullet)
		# Returns the newMagazine (which is a list of bullet object, for now)
		return newMagazine

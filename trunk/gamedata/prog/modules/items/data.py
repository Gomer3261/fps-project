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
	import modules.classes.bullets as bullets
	contents = {}
	
	# Default ammunition values
	contents["PTL"] = 36
	contents["STA"] = 150
	contents["DMR"] = 80
	contents["AMR"] = 20
	
	def getWeight(self):
		totalWeight = 0.0
		for ammoType in self.contents:
			totalWeight += self.bullets.bullets[ammoType].weight * self.contents[ammoType]
		return totalWeight
	
	def addAmmo(self, ammoType, quantity):
		"""
		Adds a quantity of ammunition to a given ammoType, 
		and returns the new quantity of ammunition.
		"""
		# If the ammo type is missing, then raise an error.
		if ammoType not in self.contents:
			raise Exception, "Inventory Error: AmmoType %s not in ammopile."%(ammoType)
			
		self.contents[ammoType] += quantity
		return self.contents[ammoType]
	
	
	def takeAmmo(self, ammoType, desiredQuantity):
		"""
		Takes ammo of specified ammoType from ammopile.
		Tries to take the full desired quantity; if there is not
		sufficient ammo in the pile to satisfy desiredQuanity, it takes
		all of the ammo available.
		"""
		
		# If the ammo type is missing, then raise an error.
		if ammoType not in self.contents:
			raise Exception, "Inventory Error: AmmoType %s not in ammopile."%(ammoType)
		if self.contents[ammoType] < 0:
			print "ERROR: Negative %s ammo quantity? wtf?"%(ammoType)
			self.contents[ammoType] = 0
		
		obtainedAmmo = 0
		
		# If there is ammo of that type...
		if self.contents[ammoType]:
			# If there is less ammo left than the magazine's capacity,
			# we fill the magazine up with all the ammo in the pile.
			if self.contents[ammoType] < desiredQuantity:
				obtainedAmmo = self.contents[ammoType]
				self.contents[ammoType] = 0
			# If there is enough ammo in the pile, then we just take it. Easy.
			else:
				obtainedAmmo = desiredQuanitity
				self.contents[ammoType] -= desiredQuanitity
		
		return obtainedAmmo
	
	
	def produceMagazine(self, ammoType, magazineCapacity):
		"""
		Returns a magazine (which is a list of bullet objects),
		filled with as many bullets possible, taken from the 
		ammopile with takeAmmo().
		"""
		# Amount of ammunition obtained
		obtainedAmmo = self.takeAmmo(ammoType, magazineCapacity)
		
		newMagazine = []
		# Makes an instance of BULLET for each bullet in obtainedAmmo.
		for i in range(obtainedAmmo):
			BULLET = self.bullets.bullets[ammoType]
			bullet = BULLET()
			newMagazine.append(bullet)
		# Returns the newMagazine (which is a list of bullet object, for now)
		return newMagazine

		
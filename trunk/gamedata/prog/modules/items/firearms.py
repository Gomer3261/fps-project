### ############################## ###
### ### ------ FIREARMS ------ ### ###
### ############################## ###
### # The FPS Project
INIT = 1








###### ------------------------------------------------------------------------------------------------------------------------------------------------
###### ######################################## ######
###### ###===----------------------------===### ######
###### ###======------ MAGAZINE ------======### ######
###### ###===----------------------------===### ######
###### ######################################## ######
###### ------------------------------------------------------------------------------------------------------------------------------------------------

class MAGAZINE:
	"""
	Magazine class. A magazine contains a list of bullets, and has a maximum capacity for them.
	"""
	contents = []
	capacity = 30
	
	def __init__(self, contents=[], capacity=30)
		self.contents = contents
		self.capacity = capacity
	
	def getBullet(self):
		if not self.contents:
			return None
		bullet = self.contents.pop(0)
		return bullet
	
	def fill(self, contents):
		self.contents = contents









###### ------------------------------------------------------------------------------------------------------------------------------------------------
###### ################################################# ######
###### ###===-------------------------------------===### ######
###### ###======------ FIREARM SIMULATOR ------======### ######
###### ###===-------------------------------------===### ######
###### ################################################# ######
###### ------------------------------------------------------------------------------------------------------------------------------------------------

class FIREARM:
	"""
	Firearm simulator. Represents and simulates the action of a modern firearm.
	"""
	
	###======------ FIREARM CONSTANTS ------======###
	isLocker = 1 # 1 if it locks the bolt back when the magazine and chamber are empty.
	
	###======------ FIREARM VARIABLES ------======###
	chamber = None # Bullet in the chamber
	magazine = None # Magazine Object
	bolt = "forward" # Position of the bolt. Either "back" or "forward"
	boltLock = 0 # If the bolt is locked in position
	hammer = "forward" # Position of the hammer. "back" or "forward"
	mode = "single" # Firing mode. auto, burst, single, safety, manual.
	lastTrigger = 0 # last time's trigger status was 0 (released)
	
	

###### ------------------------------------------------------------------------------------------------------------------------------------------------
	###########################################################
	###======------ FIREARM SIMULATOR INTERFACE ------======###
	###########################################################
###### ------------------------------------------------------------------------------------------------------------------------------------------------

	def squeezeTrigger(self):
		"""
		Calling this repeatedly is the same as just pressing and holding the trigger.
		"""
		if self.mode != "safety" and self.bolt == "forward":
			
			if self.lastTrigger == 0: # If it was Just Pressed
				if self.hammer == "forward":
					self.hammer = "back"
					print "	   Hammer cocked back"

			if self.mode == "single":
				# If we're in single fire, we only release the trigger
				# when it is just pressed
				if self.lastTrigger == 0: # If it was Just Pressed
					self.releaseHammer()
			else:
				self.releaseHammer()
			
			self.lastTrigger = 1 # Trigger was pulled



	def releaseTrigger(self):
		"""
		Releases the trigger.
		"""
		self.lastTrigger = 0 # Trigger was released
	
	
	
	def pullTrigger(self):
		"""
		Squeezes the trigger, then releases it. Not for real use; more of a debug thing.
		"""
		self.squeezeTrigger()
		self.releaseTrigger()
	
	
	
	def removeMagazine(self):
		"""
		Replaces the current magazine with a new one.
		"""
		oldMagazine = self.magazine
		self.magazine = None
		print "Magazine Removed"
		return oldMagazine
	
	
	def insertMagazine(self, newMag):
		"""
		Replaces the current magazine with a new one.
		"""
		self.magazine = newMag
		print "New magazine loaded! %s rounds in magazine."%(len(self.magazine))
	
	
	
	def cock(self):
		"""
		Slides the bolt assembly back then forth.
		If the gun is a locking gun and it's out of ammo, the bolt locks back
		"""
		self.boltBack()
		if self.isLocker:
			if (not self.magazine) and (not self.chamber):
				self.boltLock = 1
				print "The bolt locks in the back position; no loaded ammo."
		if not self.boltLock:
			self.boltForth()
	
	def boltRelease(self):
		"""
		Releases the bolt when it's locked.
		"""
		self.boltLock = 0 # Unlock the bolt
		self.boltForth() # Slide the bolt forward
	
	
	
	
###### ------------------------------------------------------------------------------------------------------------------------------------------------
	#################################################################
	###======------ FIREARM SIMULATOR PRIVATE METHODS ------======###
	#################################################################
###### ------------------------------------------------------------------------------------------------------------------------------------------------


	def releaseHammer(self):
		"""
		Releases the hammer to hit the firing pin.
		"""
		if self.hammer == "back":
			self.hammer = "forward"
			
			willFire = 0
			if self.chamber:
				if not self.chamber.fired:
					willFire = 1

			if willFire:
				self.fire()
			else:
				self.noAmmoHammerClack()
	
	
	def fire(self):
		"""
		Ignites the round's primer, burns the propellant, and fires the bullet.
		If the weapon is not in manual mode, the weapon is auto-cocked via gas operation.
		"""
		self.chamber.fired = 1
		# FIRE THE BULLET!
		print "*BANG!* BULLET FIRED!"
		if self.mode != "manual":
			print "	   Gas operated auto-cocking..."
			self.cock()


	def ammoCount(self):
		"""
		Prints out ammo information.
		"""
		cham = 0
		if self.chamber:
			cham = 1
		mag = len(self.magazine)
		print "In Chamber:", cham
		print "In Magazine:", mag
		print "Total in weapon:", cham+mag
	
	def boltBack(self):
		"""
		Slides the bolt backwards.
		Ejects any rounds in the chamber, cocks the hammer back.
		"""
		if self.chamber:
			if self.chamber.fired:
				print "	   A case has been ejected"
			else:
				print "	   An unfired bullet has been ejected"
		self.chamber = None
		self.bolt = "back"
		print "	   Bolt is in back position"
		self.hammer = "back"
		print "	   Hammer auto-cocked back"

	def boltForth(self):
		"""
		Slides the bolt forwards.
		Loads the next round from the magazine into the chamber.
		"""
		if self.magazine:
			bullet = self.magazine.getBullet()
			self.chamber = bullet
			print "	   A bullet has been loaded from the magazine into the chamber."
		self.bolt = "forward"
		print "	   Bolt is in forward position"

	def noAmmoHammerClack(self):
		"""
		This happens when the trigger mechanism fires without a loaded round.
		"""
		print "*click*: the hammer made a clacking sound. No ready round loaded."

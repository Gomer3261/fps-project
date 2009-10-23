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
	
	def __init__(self, contents=[], capacity=30):
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
	bulletType = "STA"
	fireRate = 12.0 # In Rounds Per Second
	actionTime = 1.0 / fireRate # The length of time of the weapon's automatic action.
	debug = 1
	
	###======------ FIREARM VARIABLES ------======###
	chamber = None # Bullet in the chamber
	magazine = None # Magazine Object
	bolt = "forward" # Position of the bolt. Either "back" or "forward"
	boltLock = 0 # If the bolt is locked in position
	hammer = "forward" # Position of the hammer. "back" or "forward"
	mode = "auto" # Firing mode. auto, burst, single, safety, manual.
	lastTrigger = 0 # last time's trigger status was 0 (released)
	
	###======------ INTERNAL BALLISTICS ------======###
	velocityModifier = 1.0 # This is multiplied by the bullet's regularVelocity to produce the bullet's velocity.
	stability = 1.0 # The stability the firearm provides (assumingly in the form of rifling in the barrel giving the bullet spin)
	
	
	
	def __init__(self, player):
		# The player who owns this firearm...
		self.player = player
		
		import modules.interface.terminal as terminal
		self.terminal = terminal
	
	
	
	
	def doInternalBallistics(self, bullet):
		bullet.velocity = bullet.regularVelocity * self.velocityModifier
		bullet.position = self.player.getAimOrigin()
		bullet.direction = self.player.getAimDirection()
		bullet.stability = self.stability
		bullet.owner = self.player.ticket
		

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
					if self.debug: self.terminal.output("	   Hammer cocked back")

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
		if self.debug: self.terminal.output("Magazine Removed")
		return oldMagazine
	
	
	def insertMagazine(self, newMag):
		"""
		Replaces the current magazine with a new one.
		"""
		self.magazine = newMag
		if self.debug: self.terminal.output("New magazine loaded! %s rounds in magazine."%(len(self.magazine)))
	
	
	
	def cock(self):
		"""
		Slides the bolt assembly back then forth.
		If the gun is a locking gun and it's out of ammo, the bolt locks back
		"""
		self.boltBack()
		if self.isLocker:
			if (not self.magazine) and (not self.chamber):
				self.boltLock = 1
				if self.debug: self.terminal.output("The bolt locks in the back position; no loaded ammo.")
		if not self.boltLock:
			self.boltForth()
	
	def boltRelease(self):
		"""
		Releases the bolt when it's locked.
		"""
		if self.boltLock and self.bolt == "back":
			self.boltLock = 0 # Unlock the bolt
			self.boltForth() # Slide the bolt forward
		else:
			self.terminal.output("Cannot release bolt; it's already unlocked and in the forward position.")
	
	
	
	
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
		if self.debug: self.terminal.output("*BANG!* BULLET FIRED!")
		if self.mode != "manual":
			if self.debug: self.terminal.output("	   Gas operated auto-cocking...")
			self.cock()


	def ammoCount(self):
		"""
		Prints out ammo information.
		"""
		cham = 0
		if self.chamber:
			cham = 1
		mag = len(self.magazine)
		if self.debug: self.terminal.output("In Chamber:", cham)
		if self.debug: self.terminal.output("In Magazine:", mag)
		if self.debug: self.terminal.output("Total in weapon:", cham+mag)
	
	def boltBack(self):
		"""
		Slides the bolt backwards.
		Ejects any rounds in the chamber, cocks the hammer back.
		"""
		if self.chamber:
			if self.chamber.fired:
				if self.debug: self.terminal.output("	   A case has been ejected")
			else:
				if self.debug: self.terminal.output("	   An unfired bullet has been ejected")
		self.chamber = None
		self.bolt = "back"
		if self.debug: self.terminal.output("	   Bolt is in back position")
		self.hammer = "back"
		if self.debug: self.terminal.output("	   Hammer auto-cocked back")

	def boltForth(self):
		"""
		Slides the bolt forwards.
		Loads the next round from the magazine into the chamber.
		"""
		if self.magazine:
			bullet = self.magazine.pop(0)
			self.chamber = bullet
			if self.debug: self.terminal.output("	   A bullet has been loaded from the magazine into the chamber.")
		self.bolt = "forward"
		if self.debug: self.terminal.output("	   Bolt is in forward position")

	def noAmmoHammerClack(self):
		"""
		This happens when the trigger mechanism fires without a loaded round.
		"""
		if self.debug: self.terminal.output("*click*: the hammer made a clacking sound. No ready round loaded.")

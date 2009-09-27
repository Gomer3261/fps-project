### #################################### ###
### ### ------ GUN SIMULATORS ------ ### ###
### #################################### ###
### # The FPS Project
INIT = 1

### To test it:
# Run this in IDLE so you can play with it in the python shell.
# Start calling the gun's methods to play with it.
# First, you'll want to gun.cock() it, then maybe gun.pullTrigger().
# You can change the firing mode, etc... but burst fire is not yet supported.

class GUN:
	"""
	A Gun object represents and simulates the action of a modern firearm.
	"""
	chamber = None # Bullet in the chamber
	magazine = [] # List of bullet objects
	bolt = "forward" # Position of the bolt. Either "back" or "forward"
	boltLock = 0 # If the bolt is locked in position
	hammer = "forward" # Position of the hammer. "back" or "forward"
	
	isLocker = 1 # 1 if it locks the bolt back when the magazine and chamber are empty.
	
	mode = "single" # Firing mode. auto, burst, single, safety, manual.

	lastTrigger = 0 # last time's trigger status was 0 (released)


	def pullTrigger(self):
		"""
		Squeezes the trigger, then releases it.
		"""
		self.squeezeTrigger()
		self.releaseTrigger()

	def squeezeTrigger(self):
		"""
		Calling this repeatedly is the same as just pressing and holdind the trigger.
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
	
	
	def boltRelease(self):
		"""
		Releases the bolt when it's locked.
		"""
		self.boltLock = 0 # Unlock the bolt
		self.boltForth() # Slide the bolt forward


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
			bullet = self.magazine.pop(0)
			self.chamber = bullet
			print "	   A bullet has been loaded from the magazine into the chamber."
		self.bolt = "forward"
		print "	   Bolt is in forward position"

	def noAmmoHammerClack(self):
		"""
		This happens when the trigger mechanism fires without a loaded round.
		"""
		print "*click*: the hammer made a clacking sound. No ready round loaded."

	def replaceMagazine(self, newMag):
		"""
		Replaces the current magazine with a new one.
		"""
		self.magazine = newMag
		print "New magazine loaded! %s rounds in magazine."%(len(self.magazine))









### EVERYTHING BELOW HERE IS FOR TESTING PURPOSES ONLY!!! ###

import bullets

def produceMagazine(n=30):
	mag = []
	for i in range(n):
		mag.append(bullets.STA())
	return mag

gun = GUN()

def loadMag(n=30):
	global gun
	gun.replaceMagazine(produceMagazine(n))

loadMag()



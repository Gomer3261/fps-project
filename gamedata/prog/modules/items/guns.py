### ########################## ###
### ### ------ GUNS ------ ### ###
### ########################## ###
### # The FPS Project
INIT = 1

class GUN:
	"""
	A Gun Handler. 
	Contains a firearm object. It handles the operation of a firearm in the game, 
	including animations and timing and such.
	
	In the run function, the user can start operations.
	An operation is a function which is stored in a dictionary, called operationFunctions.
	Basically, operations are timed events, where the function is called after a certain 
	amount of time has elapsed. The "-delay-" operation is a special operation, which is 
	meant only to cause a delay; it has no matching operationFunction.
	"""
	import modules.classes.firearms as firearms
	
	firearm = None
	bulletType = None
	
	player = None
	
	def __init__(self, player):
		self.player = player
		self.firearm = self.firearms.FIREARM(player)
		self.bulletType = self.firearm.bulletType
	
###### ------------------------------------------------------------------------------------------------------------------------------------------------
	#################################################################
	###======------ OPERATIONS ------======###
	#################################################################
###### ------------------------------------------------------------------------------------------------------------------------------------------------
	def reload(self, player):
		import modules.interface.terminal as terminal
		ammopile = player.inventory.ammopile
		firearm = self.firearm
		
		oldMag = firearm.removeMagazine()
		if oldMag: ammopile.addBullets(self.bulletType, len(oldMag))
		newMag = ammopile.produceMagazine(self.bulletType, 30)
		firearm.insertMagazine(newMag)
		
		### Simple Reload ###
		if not firearm.chamber:
			if firearm.boltLock:
				terminal.output("Pressing Bolt Release...")
				self.setOperation("boltRelease", 0.25)
			else:
				terminal.output("Cocking...")
				self.setOperation("cock", 0.5)
	
	def cock(self, player):
		self.firearm.cock()
	
	def boltRelease(self, player):
		self.firearm.boltRelease()
	
	

	operationFunctions = {}
	operationFunctions["reload"] = reload
	operationFunctions["cock"] = cock
	operationFunctions["boltRelease"] = boltRelease
	









###### ------------------------------------------------------------------------------------------------------------------------------------------------
	################################################
	###======------ OPERATION SYSTEM ------======###
	################################################
###### ------------------------------------------------------------------------------------------------------------------------------------------------
	operation = ""
	endTime = 0.0
	
	def runOperations(self, player):
		import time
		if self.operation:
			if time.time() >= self.endTime:
				# The operation has ended.
				operationName = self.operation
				self.setOperation()
				
				if operationName != "-delay-":
					self.operationFunctions[operationName](self, player)
				else:
					import modules.interface.terminal as terminal
					pass
	
	def setOperation(self, operation="", t=0.0):
		import time
		self.operation = operation
		self.endTime = time.time() + t
	




###### ------------------------------------------------------------------------------------------------------------------------------------------------
	##########################################
	###======------ THE RUNNER ------======###
	##########################################
###### ------------------------------------------------------------------------------------------------------------------------------------------------
	
	def run(self, player):
		"""
		The player that is using this gun handler calls this run function.
		A reference to the player object is given so that the weapon can access things 
		that are related to the player (such as the inventory's ammopile).
		"""
		firearm = self.firearm
		import modules.interface.inputs as inputs
		# The terminal, so that we know what we're doing :D
		import modules.interface.terminal as terminal
		
		
		squeezeTrigger = inputs.controller.isPositive("use")
		if squeezeTrigger:
			if not self.operation:
				firearm.squeezeTrigger()
				self.setOperation("-delay-", firearm.actionTime)
				# Each time the user squeezes the trigger, the gun's mechanisms become locked for a short period of time.
				# This is what gives the gun a rate of fire (based on firearm.actionTime)
		else:
			firearm.releaseTrigger()
		
		
		
		### INPUTS ###
		reload = inputs.controller.getStatus("reload") == 1
		cock = inputs.controller.getStatus("cock") == 1
		boltRelease = inputs.controller.getStatus("boltrelease") == 1
		
		### USER-CONTROLLED OPERATIONS ###
		if not self.operation:
			if not terminal.active:
				if reload:
					terminal.output("\nStarting reload...")
					self.setOperation("reload", 2.0)
				if cock:
					terminal.output("\nCocking...")
					self.setOperation("cock", 1.0)
				if boltRelease:
					terminal.output("\nPressing Bolt Release...")
					self.setOperation("boltRelease", 0.25)
		
		
		# Running the operation.
		self.runOperations(player)

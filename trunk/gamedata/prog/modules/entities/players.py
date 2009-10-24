############################
### ------ PLAYER ------ ###
############################
### The FPS Project
# This module runs the player object.

#import modules.interface
#terminal = modules.interface.terminal



# Easy to call method for the BGE to call to access the correct object's run() method
def run(con):
	ob = con.owner
	
	import modules
	modules.gamecontrol.localgame.players[ob[ticket]].run()







	

class PLAYER:
	LIFE = 1 # This is the object's life, not a representation of the player's life.
	# When this is == 0, it means the player object is gone, and this handler is dead and ready to be cleared.

	import GameLogic

	# DEPRECATED
	#pcol = None # The Player Collision Box (which is the parent of all of the other game objects that go along with that
	
	con = None # Controller attached to all the player object's actuators and stuff.
	
	mode = "" # The mode of the handler (either proxy or real)
	
	updateInterval = 0.1 # How often to send updates to the gamestate

	alive = 1 # Set this to 0 to kill the player.

	stance = 0 # 0=stand, 1=crouch, 2=prone
	crouchframe = 0
	
	HP = 100 # Health.
	stamina = 100 # Used for sprint bar and character fatigue effects

	speedforce = 80.0 # Speed in force of general player movement
	sprintmod = 1.75 # Speed multiplier when sprinting (1.0=no change, 2.0=double)
	crouchmod = 0.5 # Speed multiplier when crouching (sprint effects crouching speed as well)
	jumpforce = 250.0 # Upward force when jump is executed.
	slopeInfluence = 0.8 # The power of slope damping. 1.0 is pretty powerful, 2.0 makes it impossible to go up steep slopes, 0.5 makes it slight but noticeable.
	noTouchMod = 0.02 # The modifier on desired movement when the player is not touching the ground.


	def __init__(self, ticket, spawnObj, mode="proxy"):
		self.mode = mode
		self.ticket = ticket
		
		if self.mode == "proxy":
			self.proxyInit(spawnObj)
		elif self.mode == "real":
			self.realInit(spawnObj)
		else:
			raise ValueError("No acceptable init found for mode: %s" % mode)
	
	
	
		
	def proxyInit(self, spawnObj):
		self.spawnObj = spawnObj
		
		# Spawning the player proxy object
		self.gameObject = self.spawnGameObject("playerProxy")
		con = self.gameObject.controllers[0]
		
		# Getting some related objects
		self.YPivot = con.actuators["YPivot"].owner
		self.centerhinge = con.actuators["centerhinge"].owner
		self.fpcam = con.actuators["fpcam"].owner
		self.trueAim = con.actuators["trueAim"].owner
	
	def realInit(self, spawnObj):
		import modules
		
		self.spawnObj = spawnObj

		# Spawning the player object
		self.gameObject = self.spawnGameObject("playerReal")
		con = self.gameObject.controllers[0]

		# Getting some related objects
		self.YPivot = con.actuators["YPivot"].owner
		self.centerhinge = con.actuators["centerhinge"].owner
		self.fpcam = con.actuators["fpcam"].owner
		self.trueAim = con.actuators["trueAim"].owner


		# Getting the foot sensors
		self.feet = []
		self.feet.append(con.sensors["foot1"])
		self.feet.append(con.sensors["foot2"])
		self.feet.append(con.sensors["foot3"])
		self.feet.append(con.sensors["foot4"])
		self.feet.append(con.sensors["foot5"])
		
		# Getting the roof sensors (should be renamed to ceiling detectors?)
		self.roofDetectors = []
		self.roofDetectors.append(con.sensors["roofDetector1"])
		self.roofDetectors.append(con.sensors["roofDetector2"])
		self.roofDetectors.append(con.sensors["roofDetector3"])
		self.roofDetectors.append(con.sensors["roofDetector4"])
		self.roofDetectors.append(con.sensors["roofDetector5"])
		
		# A timer for knowing when to update (networking)
		self.updateTimer = modules.timetools.TIMER()

		# Various modules (use of these deprecated?)
		self.inputs = modules.interface.inputs
		self.terminal = modules.interface.terminal
		self.options = modules.interface.options
		self.mousetools = modules.gamesystems.mousetools
		self.damper = modules.gamesystems.damper
		
		
		# Okay, now we make an inventory for the player :)
		import modules.items.inventory as inventoryModule
		self.inventory = inventoryModule.INVENTORY(self)
		#print "Player Inventory Created."
		#print "Ammopile weighs in at %.1f kilograms." % (self.inventory.ammopile.getWeight())








	### ========================================================================
	### SPAWN PLAYER OBJECT
	### ========================================================================
	
	def spawnGameObject(self, name="playerobject"):
		scene = self.GameLogic.getCurrentScene()
		obj = scene.addObject(name, self.spawnObj)
		obj.position = [0.0, 0.0, 10.0]
		obj.orientation = [[1,0,0],[0,1,0],[0,0,1]]
		return obj
		


	
	
	
	
	
	### ========================================================================
	### USEFUL FUNCTIONS
	### ========================================================================
	
	def getAimOrigin(self):
		pos = self.trueAim.position
		return pos
	
	def getAimDirection(self):
		ori = self.trueAim.orientation
		YX = ori[0][1]
		YY = ori[1][1]
		YZ = ori[2][1]
		direction = [YX, YY, YZ]
		return direction







	### ========================================================================
	### HIGH-LEVEL RUN FUNCTION
	### ========================================================================

	def run(self):
		import modules
		gamestate = modules.gamecontrol.gamestate.gamestate
		
		### MANAGES THE PLAYER ###
		if gamestate.playerIsInGame(self.ticket):
			# When they're in gamestate, call the do method
			if self.mode == "proxy":
				self.doProxy()
			elif self.mode == "real":
				self.doReal()
			else:
				raise ValueError("No acceptable do() found for mode: %s" % self.mode)
		else:
			# When they are NOT in the gamestate, doDeath().
			self.doDeath()
			
	def doProxy(self):
		self.doReplication() # Replicating the current gamestate

	def doReal(self):
		self.doReplication() # Nothing for doReal yet.
		self.doPlayerStance() # Checking and applying different player stances.
		self.doPlayerMovement() # Running, Sprinting, Jumping, etc...
		self.doMouseLook() # Looking around with mouse in first person...
		self.doUpdate() # Send updates to the gamestate
		
		self.doInventory() # Managing the player's inventory (switching weapons, etc)
		#self.doInteraction() # Using current selected inventory item, interacting with buttons, etc..




	### ========================================================================
	### DO REPLICATION
	### ========================================================================
	
	def doReplication(self):
		import modules
		gamestate = modules.gamecontrol.gamestate.gamestate
		localgame = modules.gamecontrol.localgame
		
		if self.mode == "proxy":
			from Mathutils import Vector
			
			### REPLICATING POSITION ###
			self.gameObject.position = gamestate.contents["P"][self.ticket]["A"]["P"]
			
			### REPLICATING ORIENTATION ###
			v = gamestate.contents["P"][self.ticket]["A"]["O"]
			try:
				v[2] = 0
			except:
				pass
			
			y = Vector(v[0], v[1], v[2])
			z = Vector([0, 0, 1])
			x = y.cross(z)
			
			mat = [
				[x[0], y[0], z[0]],
				[x[1], y[1], z[1]],
				[x[2], y[2], z[2]]
				]
				
			self.gameObject.localOrientation = mat





	### ========================================================================
	### DO UPDATE
	### ========================================================================
	
	def doUpdate(self):
		if self.updateTimer.do(self.updateInterval):
			import modules
			router = modules.gamecontrol.director.router
			
			# Position
			posVec = self.gameObject.position[:]
			
			# Orientation
			oriVec = self.gameObject.getAxisVect((0, 1, 0))
			
			# Attribute dictionary
			A = {}
			A["P"] = posVec
			A["O"] = oriVec

			# Throw the data
			#print "THROWING DATA TO ROUTER"
			router.throw(["upa", [self.ticket, A]])
	
	
	
	
	
	
	
	### ========================================================================
	### DO INVENTORY
	### ========================================================================
	
	def doInventory(self):
		# Just calling the active item's run method..
		active = self.inventory.getActiveItem()
		active.run(self)








	### ========================================================================
	### DO PLAYER STANCE
	### ========================================================================

	def doPlayerStance(self):
	
		self.findStance()
		
		#apply stance
		if self.stance == 1:
			self.crouch()
		else:
			self.stand()
	
	
				
	def findStance(self):
		crouch = self.inputs.controller.getStatus("crouch")
		crouchType = self.options.settings["crouch"]
		
		if crouchType == "Hold" and crouch:
			self.stance = 1
		
		elif crouchType == "Toggle":
			if crouch == 1:
				if self.stance != 1:
					self.stance = 1
				elif not self.detectRoof():
					self.stance = 0
					
		elif not self.detectRoof():
			self.stance = 0
			
			
	def detectRoof(self):
		for i in self.roofDetectors:
			if i.positive:
				return 1
						
						
	def crouch(self):
		import modules
		#modules.interface.terminal.output("crouching")
		crouchamount = 0.0
		
		if self.crouchframe < 10:
			self.crouchframe += 1
			crouchamount = self.crouchframe * 0.04
		
			self.gameObject.localScale = [1.0, 1.0, (1.0 - crouchamount)]
		
		
		
	def stand(self):
		import modules
		#modules.interface.terminal.output("standing")
		crouchamount = 0.0
		
		if self.crouchframe > 0:
			self.crouchframe -= 1.0
			crouchamount = self.crouchframe * 0.04
		
			self.gameObject.localScale = [1.0, 1.0, (1.0 - crouchamount)]
		
		
	
	
	
	
	
	### ========================================================================
	### DO PLAYER MOVEMENT
	### ========================================================================

	def doPlayerMovement(self):
		"""
		Does player movement.
		"""
		
		
		
		movement = self.getDesiredMovement()
		
		movement = self.applySprint(movement)
		movement = self.applyStance(movement)
		movement = self.doSlopeDamping(movement)
		movement = self.degradeMovementWhenNotOnTheGround(movement)

		# Applying the movement
		if not self.terminal.active:
			self.gameObject.applyForce(movement, 1)

		self.doDamping()

	
	

	def getDesiredMovement(self):
		"""
		Gets the player's desired movement (based on inputs)
		in local coords
		"""

		
		# Initial Movement Values (in local coords)
		X = 0.0
		Y = 0.0
		Z = 0.0



		# Input Status
		con = self.con
		
		forward = self.inputs.controller.isPositive("forward")
		backward = self.inputs.controller.isPositive("backward")
		left = self.inputs.controller.isPositive("left")
		right = self.inputs.controller.isPositive("right")
		
		jump = self.inputs.controller.getStatus("jump")



		# Figuring out desired movement
		if forward:
			Y += self.speedforce
		if backward:
			Y -= self.speedforce

		if left:
			X -= self.speedforce
		if right:
			X += self.speedforce

		if X and Y:
			X *= 0.7071
			Y *= 0.7071

		if (jump == 1) and self.isOnTheGround():
			Z = self.jumpforce

		return [X, Y, Z]





	def localToGlobal(self, V):
		return self.postMultiply(V)

	def postMultiply(self, V):
		"""
		Converts Local to Global Coords
		"""
		import Mathutils

		# Getting the Orientation
		ori = self.gameObject.orientation[:]
		l1 = ori[0]
		l2 = ori[1]
		l3 = ori[2]
		matrix = Mathutils.Matrix(l1, l2, l3)

		# Getting the original vector object
		originalVector = Mathutils.Vector(V)

		# Post-multiplication to get newVector
		newVector = matrix * originalVector

		return [newVector.x, newVector.y, newVector.z]




	def globalToLocal(self, V):
		return self.preMultiply(V)
	
	def preMultiply(self, V):
		"""
		Converts Global to Local Coords
		"""
		import Mathutils

		# Getting the Orientation
		ori = self.gameObject.orientation[:]
		l1 = ori[0]
		l2 = ori[1]
		l3 = ori[2]
		matrix = Mathutils.Matrix(l1, l2, l3)

		# Getting the original vector object
		originalVector = Mathutils.Vector(V)

		# Pre-multiplication to get newVector
		newVector = originalVector * matrix

		return [newVector.x, newVector.y, newVector.z]





		

	def applySprint(self, movement):
		"""
		Multiplies movement by the sprintmod value when the sprint button is held.
		"""
		newMovement = movement[:] # Making a copy, not a reference
		sprint = self.inputs.controller.isPositive("sprint")
		if sprint:
			for i in range(2):
				newMovement[i] = movement[i] * self.sprintmod
		#newMovement[2] = movement[2] # Leaves Z axis movement unchanged (jumping)
		return newMovement
		
		
		
	def applyStance(self, movement):
		newMovement = movement[:]
		
		#apply crouch
		if self.stance == 1:
			for i in range(2):
				newMovement[i] = movement[i] * self.crouchmod
		
		return newMovement
		
	

	def degradeMovementWhenNotOnTheGround(self, movement):
		if self.isOnTheGround():
			return movement
		else:
			for i in range(3):
				movement[i] *= self.noTouchMod
			return movement


	def doDamping(self):
		"""
		Applies damping to the character so that they do not slide around
		like they are on glass.
		"""
		damp = 1.0
		if self.isOnTheGround():
			# Damping Operation
			damp = 25.0
		else:
			damp = 0.5
		self.damper.dampXY(self.gameObject, damp)
		


	def getFloorNormal(self):
		"""
		Gets the average normal of the floor
		"""
		
		# Gathering the hitNormals from each foot
		normals = []
		for foot in self.feet:
			if foot.positive:
				normals.append(foot.hitNormal)

		# Averaging the hitNormals in normals
		avgnormal = [0.0, 0.0, 0.0]
		if len(normals) > 0:
			for normal in normals:
				for i in range(3):
					avgnormal[i] += normal[i]
			for i in range(3):
				avgnormal[i] /= len(normals)
				# avgnormal[i] *= -1 # ?

		return avgnormal

	def isOnTheGround(self):
		"""
		Tells you if at least one foot is on the ground.
		Returns 1 if a foot is on the ground.
		Returns 0 if no feet are touching the ground.
		"""
		onGround = 0
		for foot in self.feet:
			if foot.positive:
				onGround = 1
				break
		return onGround
	

	def getSlopeFactor(self, m):
		"""
		Gets the slope factor.
		0.0 means no effect on movement speed.
		-0.5 would be a slow-down of movement speed (going uphill)
		0.5 would be a boost of movement speed (doing downhill)
		"""
		import Mathutils
		import math

		movement = m[:] # Making a copy

		movement[2] = 0.0

		if movement == [0.0, 0.0, 0.0]: return 0.0

		movementVector = Mathutils.Vector(movement)
		movementVector.normalize()

		floorNormal = self.getFloorNormal()
		floorVector = Mathutils.Vector( self.globalToLocal(floorNormal) )

		return floorVector.dot(movementVector)

	def applySlopeFactor(self, movement, slopeFactor):
		"""
		Applies a given slopeFactor to a desired movement vector.
		Returns the new movement.
		"""
		
		newMovement = movement[:]

		# For X and Y
		for i in range(2):
			slopeVelocity = movement[i] * slopeFactor
			newMovement[i] = movement[i] + slopeVelocity


		### Jumping Stuff ###
		# Slopes can never make your jumps higher..
		if slopeFactor < 0.0:
			slopeVelocity = movement[2] * slopeFactor
			newMovement[2] = movement[2] + slopeVelocity
		# You cannot jump up steep slopes.
		if slopeFactor < -0.25:
			newMovement[2] = 0.0

		return newMovement

	def doSlopeDamping(self, movement):
		if self.isOnTheGround():
			slopeFactor = self.getSlopeFactor(movement)
			slopeFactor *= self.slopeInfluence
			
			# Maximum negative slope...
			if slopeFactor < -0.5:
				slopeFactor = -1.0
				
			newMovement = self.applySlopeFactor(movement, slopeFactor)
			return newMovement
		else:
			return movement
		
		







	### ========================================================================
	### DO MOUSELOOK
	### ========================================================================

	def doMouseLook(self):
		##################################
		### ------ Mouse Script ------ ###
		##################################
		# By Chase Moskal

		#====================
		#===   Settings   ===
		#====================

		# X and Y Sensitivity
		mxsens = 5.0
		mysens = 5.0

		# Invert X and/or Y axes?
		invertX = 0
		invertY = 0

		# Settings Override
		import traceback
		try:
			mxsens = self.options.settings["mxsens"]
			mysens = self.options.settings["mysens"]
			invertX = self.options.settings["invertx"]
			invertY = self.options.settings["inverty"]
		except:
			traceback.print_exc()
			print "Player/HANDLER/doMouseLook: Unable to get mouse settings from options.\n"
		
		# Restrict Y axis? (disallow looking upside-down?)
		restrictY = 1



		#=========================
		#===   getting stuff   ===
		#=========================

		import GameLogic as gl
		import Rasterizer
		mousetools = self.mousetools


		

		# For an FPS, set the player collision box to Xpivot,
		# and set up an empty as the Y pivot.
		Ypivot = self.YPivot
		Xpivot = self.gameObject




		#=================================
		#===   Real Mouselook Action   ===
		#=================================

		# Little function to check if something
		# is positive (>=0)
		def isPositive(x):
			if x >= 0.0:
				return 1
			return 0


		# Shortcut to the mouse object
		mouse = mousetools.mouse
		# Hiding the mouse cursor
		mouse.hide()



		if True:
			
			# Getting mouse movement...
			Xmovement, Ymovement = mouse.getMovement()
			
			# Converting sensitivity to lower terms
			Xc = mxsens * 0.001
			Yc = mysens * 0.001
			
			# Getting the rotation values.
			X = -float(Xmovement) * Xc
			Y = float(Ymovement) * Yc
			
			# Inversions
			if invertX:
				X *= -1
			if invertY:
				Y *= -1
			
			# Getting orientation matrix
			# information that will determine the
			# mouselook Y restrictions.
			
			isMovingUp = isPositive(Y) # checks if the mouse movement is currently up (1) or down (0)
			
			ori = Ypivot.orientation
			
			# Getting uprightness.
			ZZ = ori[2][2] # Z axis' Z component
			isUpright = isPositive(ZZ) # 1 means it's upright, 0 means it's upside-down.
			
			# Getting the facing upness
			YZ = ori[2][1] # Y axis' Z component
			isFacingUp = isPositive(YZ)
			# Imagine the user on a perfectly smooth floor that spans infinitely into the distance.
			# isFacingUp tells you if the player is looking at the floor (0), or at the sky (1).
			
			
			
			
			#===============================
			#===   Applying X Rotation   ===
			#===============================
			
			# If we're not restricting the Y axis, and we're upside down,
			# then we need to invert the X axis mouse movement.
			if (not restrictY) and (not isUpright):
				Xpivot.applyRotation([0, 0, -X], 0)
			else:
				Xpivot.applyRotation([0, 0, X], 0)
			
			
			#===============================
			#===   Applying Y Rotation   ===
			#===============================
			if restrictY:
				# Y Axis is restricted
				
				# Only allows movement while upright
				if isUpright:
					Ypivot.applyRotation([Y, 0, 0], 1)
				
				# While not upright and you're facing down, allow you to look up again
				elif isMovingUp and not isFacingUp:
					Ypivot.applyRotation([Y, 0, 0], 1)
				
				# While not upright and you're facing up, allow you to look down again
				elif not isMovingUp and isFacingUp:
					Ypivot.applyRotation([Y, 0, 0], 1)
			
			else:
				# Y Axis is NOT restricted
				Ypivot.applyRotation([Y, 0, 0], 1)









	### ========================================================================
	### DO DEATH
	### ========================================================================
	
	
	def doDeath(self):
		if self.mode == "proxy":
			self.doProxyDeath()
		elif self.mode == "real":
			self.doRealDeath()
		else:
			raise ValueError("No acceptable doDeath() found for mode: %s" % self.mode)
			

	def doProxyDeath(self):
		if self.LIFE:
			# Kill the game object
			self.gameObject.endObject()
			
			# Kill the handle
			import modules
			modules.gamecontrol.localgame.players.deletePlayer(self.ticket)
			
			# Set the LIFE to 0, this object is completely dead
			self.LIFE = 0
			
			
	def doRealDeath(self):
		if self.LIFE:
			scene = self.GameLogic.getCurrentScene()
			if scene.active_camera != self.fpcam:
				# Kill the game object
				self.gameObject.endObject()
				
				# Kill the handle
				import modules
				modules.gamecontrol.localgame.players.deletePlayer(self.ticket)
				
				# Set the LIFE to 0, this object is completely dead
				self.LIFE = 0
				

		

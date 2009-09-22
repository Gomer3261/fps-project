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

	pcol = None # The Player Collision Box (which is the parent of all of the other game objects that go along with that
	con = None # Controller attached to all the player object's actuators and stuff.
	
	mode = "" # The mode of the handler (either proxy or real)

	alive = 1 # Set this to 0 to kill the player.

	stance = 0 # 0=stand, 1=crouch, 2=prone
	HP = 100 # Health.
	stamina = 100 # Used for sprint bar and character fatigue effects

	speedforce = 80.0 # Speed in force of general player movement
	sprintmod = 1.75 # Speed multiplier when sprinting (1.0=no change, 2.0=double)
	jumpforce = 200.0 # Upward force when jump is executed.
	slopeInfluence = 0.5 # The power of slope damping. 1.0 is pretty powerful, 2.0 makes it impossible to go up steep slopes, 0.5 makes it slight but noticeable.
	noTouchMod = 0.02 # The modifier on desired movement when the player is not touching the ground.


	def __init__(self, ticket, spawnObj, mode = "proxy"):
		self.mode = mode
		self.ticket = ticket
		
		if mode == "proxy":
			self.proxyInit(spawnObj)
		elif mode == "real":
			self.realInit(spawnObj)
		else:
			raise ValueError("No acceptable init found for mode: %s" % mode)
	
	
	
		
	def proxyInit(self, spawnObj):
		self.spawnObj = spawnObj
		
		# Spawning the player proxy object
		self.gameObj = self.spawnGameObj("playerProxy")
	
	def realInit(self, spawnObj):
		import modules
		
		self.spawnObj = spawnObj

		# Spawning the player object
		self.gameObj = self.spawnGameObj("playerReal")
		
		con = self.gameObj.controllers[0]

		# Getting some related objects
		self.YPivot = con.actuators["YPivot"].owner
		self.centerhinge = con.actuators["centerhinge"].owner
		self.fpcam = con.actuators["fpcam"].owner

		# Getting the foot sensors
		self.feet = []
		self.feet.append(con.sensors["foot1"])
		self.feet.append(con.sensors["foot2"])
		self.feet.append(con.sensors["foot3"])
		self.feet.append(con.sensors["foot4"])
		self.feet.append(con.sensors["foot5"])

	
		self.inputs = modules.interface.inputs
		self.terminal = modules.interface.terminal
		self.options = modules.interface.options

		self.mousetools = modules.gamesystems.mousetools
		self.damper = modules.gamesystems.damper








	### ========================================================================
	### SPAWN PLAYER OBJECT
	### ========================================================================
	
	def spawnGameObj(self, name="playerobject"):
		scene = self.GameLogic.getCurrentScene()
		obj = scene.addObject(name, self.spawnObj)
		obj.position = [0.0, 0.0, 10.0]
		obj.orientation = [[1,0,0],[0,1,0],[0,0,1]]
		return obj
		











	### ========================================================================
	### HIGH-LEVEL RUN FUNCTION
	### ========================================================================

	def run(self):
		if self.alive:
			self.doReplication() # Replicating the current gamestate
			
			if self.mode == "proxy":
				self.doProxy()
			elif self.mode == "real":
				self.doReal()
			else:
				raise ValueError("No acceptable do() found for mode: %s" % mode)
		else:
			self.doDeath()
			
	def doProxy(self):
		pass #self.doReplication() # Replicating the current gamestate

	def doReal(self):
		self.doCamera() # Deprecated
		self.doPlayerMovement() # Running, Sprinting, Jumping, etc...
		self.doMouseLook() # Looking around with mouse in first person...
		#self.doInventory() # Managing the player's inventory (switching weapons, etc)
		#self.doInteraction() # Using current selected inventory item, interacting with buttons, etc..




	### ========================================================================
	### DO REPLICATION
	### ========================================================================
	
	def doReplication(self):
		import modules
		gamestate = modules.gamecontrol.gamestate.gamestate
		
		if not gamestate.playerIsInGame(self.ticket):
			self.alive = 0



	### ========================================================================
	### DO CAMERA (Deprecated)s
	### ========================================================================
	
	def doCamera(self):
		# Deprecated
		pass
		# Just sets the camera
##        if self.LIFE:
##            scene = self.GameLogic.getCurrentScene()
##            if scene.active_camera != self.fpcam:
##                scene.active_camera = self.fpcam








	### ========================================================================
	### DO PLAYER MOVEMENT
	### ========================================================================

	def doPlayerMovement(self):
		"""
		Does player movement.
		"""
		
		movement = self.getDesiredMovement()
		
		movement = self.applySprint(movement)
		movement = self.doSlopeDamping(movement)
		movement = self.degradeMovementWhenNotOnTheGround(movement)

		# Applying the movement
		if not self.terminal.active:
			self.gameObj.applyForce(movement, 1)

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
		
		forward = self.inputs.controller.getStatus("forward")
		backward = self.inputs.controller.getStatus("backward")
		left = self.inputs.controller.getStatus("left")
		right = self.inputs.controller.getStatus("right")
		
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
		ori = self.gameObj.orientation[:]
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
		ori = self.gameObj.orientation[:]
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
		self.damper.dampXY(self.gameObj, damp)
		


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
			newMovement = self.applySlopeFactor(movement, slopeFactor)
			return newMovement
		else:
			return movement
		
		







	### ========================================================================
	### DO MOUSE LOOK
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
		Xpivot = self.gameObj




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
		if self.LIFE:
			scene = self.GameLogic.getCurrentScene()
			if scene.active_camera != self.fpcam:
				self.gameObj.endObject()
				# Kill the handle
				import modules
				modules.gamecontrol.localgame.players.deletePlayer(self.ticket)
				self.LIFE = 0

		

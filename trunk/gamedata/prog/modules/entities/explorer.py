##############################
### ------ EXPLORER ------ ###
##############################
### The FPS Project
# This module runs the explorer object.

#import modules.interface
#terminal = modules.interface.terminal



# Easy to call method for the BGE to call to access the correct object's run() method
def run(con):
	ob = con.owner
	
	import modules
	modules.gamecontrol.localgame.explorer.run()







	

class EXPLORER:
	LIFE = 1 # This is the object's life, not a representation of the player's life.
	# When this is == 0, it means the player object is gone, and this handler is dead and ready to be cleared.

	import GameLogic
	
	con = None # Controller attached to all the player object's actuators and stuff.

	alive = 1 # Set this to 0 to kill the explorer.

	speed = 0.1 # Speed in blender units of general explorer movement
	sprintmod = 3.0 # Speed multiplier when sprinting (1.0=no change, 2.0=double)


	def __init__(self, spawnObj):

		import modules
		
		self.spawnObj = spawnObj

		# Spawning the explorer object
		self.gameObject = self.spawnGameObject("explorer")
		
		con = self.gameObject.controllers[0]

		# Getting some related objects
		self.YPivot = con.actuators["YPivot"].owner
		self.fpcam = con.actuators["fpcam"].owner

		# Various modules.
		self.inputs = modules.interface.inputs
		self.terminal = modules.interface.terminal
		self.options = modules.interface.options

		self.mousetools = modules.gamesystems.mousetools








	### ========================================================================
	### SPAWN EXPLORER OBJECT
	### ========================================================================
	
	def spawnGameObject(self, name="playerobject"):
		scene = self.GameLogic.getCurrentScene()
		obj = scene.addObject(name, self.spawnObj)
		obj.position = [0.0, 0.0, 10.0]
		obj.orientation = [[1,0,0],[0,1,0],[0,0,1]]
		return obj
		











	### ========================================================================
	### HIGH-LEVEL RUN FUNCTION
	### ========================================================================

	def run(self):
		import modules
		#info = modules.gamecontrol.info
		#gamestate = modules.gamecontrol.gamestate.gamestate
	
		if self.alive:
			self.do()
		else:
			self.doDeath()

	def do(self):
		self.doMovement() # Running, Sprinting, Jumping, etc...
		self.doMouseLook() # Looking around with mouse in first person...




	
	### ========================================================================
	### DO PLAYER MOVEMENT
	### ========================================================================

	def doMovement(self):
		"""
		Does player movement.
		"""
		movement = self.getDesiredMovement()
		movement = self.applySprint(movement)

		# Applying the movement
		if not self.terminal.active:
			# Local XY Movement
			self.gameObject.applyMovement([movement[0], movement[1], 0.0], 1)
			# Global Z (Rise/Sink) Movement.
			self.gameObject.applyMovement([0.0, 0.0, movement[2]], 0)

	
	

	def getDesiredMovement(self):
		"""
		Gets the explorer's desired movement (based on inputs)
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

		# Figuring out desired movement
		if forward:
			Y += self.speed
		if backward:
			Y -= self.speed

		if left:
			X -= self.speed
		if right:
			X += self.speed

		if X and Y:
			X *= 0.7071
			Y *= 0.7071
		
		Z = self.getDesiredRiseOrSink()

		return [X, Y, Z]
	
	
	def getDesiredRiseOrSink(self):
		"""
		Gets the explorer's desired movement for sinking and rising (in global coords)
		"""
		# Initial Movement Values (in local coords)
		Z = 0.0
		
		# Input Status
		con = self.con
		up = self.inputs.controller.isPositive("rise")
		down = self.inputs.controller.isPositive("sink")

		if up:
			Z += self.speed
		if down:
			Z -= self.speed

		return Z


	def applySprint(self, movement):
		"""
		Multiplies movement by the sprintmod value when the sprint button is held.
		"""
		newMovement = movement[:] # Making a copy, not a reference
		sprint = self.inputs.controller.isPositive("sprint")
		if sprint:
			for i in range(3):
				newMovement[i] *= self.sprintmod

		return newMovement
		
		







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
		Ypivot = self.gameObject
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
		if self.LIFE:
			scene = self.GameLogic.getCurrentScene()
			if scene.active_camera != self.fpcam:
				# Kill the game object
				self.gameObject.endObject()
				
				# Kill the handle
				import modules
				modules.gamecontrol.localgame.explorers.explorer = None
				
				# Set the LIFE to 0, this object is completely dead
				self.LIFE = 0

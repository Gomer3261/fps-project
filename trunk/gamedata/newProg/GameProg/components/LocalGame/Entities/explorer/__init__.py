### Explorer Entity ###

class Class:
	def __init__(self, EID, LocalGame):
		self.EID = EID
		self.LocalGame = LocalGame
		self.GameState = LocalGame.GameState
		self.Networking = LocalGame.Networking
		self.Interface = LocalGame.Interface
		
		# Initiating the gameObject
		import GameLogic as gl
		own = gl.getCurrentController().owner
		self.gameObject = gl.getCurrentScene().addObject("explorer", own)
		
		# The gameObject acts as both the XPivot and the YPivot for the explorer.
		self.XPivot = self.gameObject
		self.YPivot = self.gameObject
		
		
		print("Explorer Initiated.")
	
	def end(self):
		self.gameObject.endObject()
		self.gameObject = None
		print("Explorer Entity Ended.")
	
	def run(self):
		self.doMouseLook()
		X, Y, Z = self.getDesiredLocalMovement()
		self.gameObject.applyMovement( (X,Y,0), 1 ) # X and Y applied locally.
		self.gameObject.applyMovement( (0,0,Z), 0 ) # Z applied globally.
	
	def getDesiredLocalMovement(self):
		Controller = self.Interface.Inputs.Controller
		
		SPEED = 0.5
		MOD = 4.0
		
		if Controller.isPositive('sprint'): SPEED *= MOD
		
		X = 0
		Y = 0
		Z = 0
		
		if Controller.isPositive('forward'): Y += SPEED
		if Controller.isPositive('backward'): Y -= SPEED
		if Controller.isPositive('left'): X -= SPEED
		if Controller.isPositive('right'): X += SPEED
		if Controller.isPositive('rise'): Z += SPEED
		if Controller.isPositive('sink'): Z -= SPEED
		
		return X, Y, Z
		
		
	
	def doMouseLook(self):
		"""
		Does the MouseLook.
		"""

		#====================
		#===   Settings	  ===
		#====================

		# X and Y Sensitivity
		mxsens = 5.0
		mysens = 5.0

		# Invert X and/or Y axes?
		invertX = 0
		invertY = 0

		# Restrict Y axis? (disallow looking upside-down?)
		restrictY = 1
		
		

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
		Mouse = self.Interface.Inputs.Mouse
		# Hiding the mouse cursor
		Mouse.hide()




		
		# Getting mouse movement...
		Xmovement, Ymovement = Mouse.getMovement()
		
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
		
		ori = self.YPivot.orientation
		
		# Getting uprightness.
		ZZ = ori[2][2] # Z axis' Z component
		isUpright = isPositive(ZZ) # 1 means it's upright, 0 means it's upside-down.
		
		# Getting the facing upness
		YZ = ori[2][1] # Y axis' Z component
		isFacingUp = isPositive(YZ)
		# Imagine the user on a perfectly smooth floor that spans infinitely into the distance.
		# isFacingUp tells you if the player is looking at the floor (0), or at the sky (1).
		
		
		
		
		#===============================
		#===   Applying X Rotation	 ===
		#===============================
		
		# If we're not restricting the Y axis, and we're upside down,
		# then we need to invert the X axis mouse movement.
		if (not restrictY) and (not isUpright):
			self.XPivot.applyRotation([0, 0, -X], 0)
		else:
			self.XPivot.applyRotation([0, 0, X], 0)
		
		
		
		
		
		#===============================
		#===   Applying Y Rotation	 ===
		#===============================
		if restrictY:
			# Y Axis is restricted
			
			# Only allows movement while upright
			if isUpright:
				self.YPivot.applyRotation([Y, 0, 0], 1)
			
			# While not upright and you're facing down, allow you to look up again
			elif isMovingUp and not isFacingUp:
				self.YPivot.applyRotation([Y, 0, 0], 1)
			
			# While not upright and you're facing up, allow you to look down again
			elif not isMovingUp and isFacingUp:
				self.YPivot.applyRotation([Y, 0, 0], 1)
		
		else:
			# Y Axis is NOT restricted
			self.YPivot.applyRotation([Y, 0, 0], 1)

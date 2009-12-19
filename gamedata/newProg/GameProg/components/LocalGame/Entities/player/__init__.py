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
		self.gameObject = gl.getCurrentScene().addObject("player_real", own)
		self.cont = self.gameObject.controllers[0]
		
		# Getting the Camera
		self.cam = self.cont.actuators["cam"].owner
		
		# The gameObject acts as both the XPivot and the YPivot for the explorer.
		self.XPivot = self.gameObject
		self.YPivot = self.gameObject
		
		self.YValue = 500.0 # 1.0 = straight down, 1000.0 = straight up
		
		print("Player Initiated")
	
	def end(self):
		self.LocalGame.Camera.clear()
		self.gameObject.endObject()
		self.gameObject = None
		print("Player Entity Ended")
	
	
	
	def run(self):
		# Camera Management
		self.LocalGame.Camera.set(self.cam)
		self.suicideControlLoop()
		self.doMouseLook()
		
		# Movement can only occur when the terminal is not active.
		if not self.Interface.Terminal.active:
			X, Y, Z = self.getDesiredLocalMovement()
	
	
	def suicideControlLoop(self):
		if not self.Interface.Terminal.active:
			suicideStatus = self.Interface.Inputs.Controller.getStatus("suicide")
			if suicideStatus == 1:
				# Suicide!
				package = ['GS', ['AR', ['RE', self.EID]]]
				self.Networking.gpsnet.send(package)
				print("Remove Player Entity request sent via Networking.gpsnet.send(request)...")
	
	
	
	
	def getDesiredLocalMovement(self):
		Controller = self.Interface.Inputs.Controller
		
		SPEED = 0.1
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

		#====================#
		#===   Settings	  ===#
		#====================#

		# X and Y Sensitivity
		mxsens = 5.0
		mysens = 5.0

		# Invert X and/or Y axes?
		invertX = 0
		invertY = 0

		# Restrict Y axis? (disallow looking upside-down?)
		restrictY = 1
		
		

		#=================================#
		#===   Real Mouselook Action   ===#
		#=================================#

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
		
		
		#===============================#
		#===   Applying X Rotation	 ===#
		#===============================#
		self.XPivot.applyRotation([0, 0, X], 0)
		
		#===============================#
		#===   Applying Y Rotation	 ===#
		#===============================#
		self.YValue += Y

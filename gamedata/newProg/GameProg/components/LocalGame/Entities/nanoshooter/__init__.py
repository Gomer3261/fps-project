### Nanoshooter Entity ###

class Class:
	def __init__(self, EID, LocalGame):
		self.type = "nanoshooter"
		self.EID = EID
		self.LocalGame = LocalGame
		
		self.GameState = LocalGame.GameState
		self.Networking = LocalGame.Networking
		self.Interface = LocalGame.Interface
		self.Resources = LocalGame.Resources
		
		# Initiating the gameObject
		import GameLogic as gl
		own = gl.getCurrentController().owner
		self.gameObject = gl.getCurrentScene().addObject("nanoshooter", own)
		# Initiating the Aimpoint
		self.aimPoint = gl.getCurrentScene().addObject("ns_aimPoint", own)
		
		# Getting the Controller
		self.cont = self.gameObject.controllers[0]
		# Getting the Sensors
		self.mouseOver = self.cont.sensors["mouseOver"]
		# Getting the Camera
		self.cam = self.cont.actuators["cam"].owner
		
		print("Nanoshooter Initiated.")
	
	def end(self):
		self.LocalGame.Camera.clear()
		self.aimPoint.endObject()
		self.aimPoint = None
		self.gameObject.endObject()
		self.gameObject = None
		print("Nanoshooter Entity Ended.")
	
	def run(self):
		# Camera Management
		self.LocalGame.Camera.set(self.cam)
		self.suicideControlLoop()
		self.aimControl()
		
		# Movement can only occur when the terminal is not active.
		if not self.Interface.Terminal.active:
			X, Y, Z = self.getDesiredLocalMovement()
			self.gameObject.applyForce( (X,Y,Z), 0 )
			self.Resources.Tools.Damper.dampXY(self.gameObject, 20.0)
	
	def suicideControlLoop(self):
		if not self.Interface.Terminal.active:
			suicideStatus = self.Interface.Inputs.Controller.getStatus("suicide")
			if suicideStatus == 1:
				# Suicide!
				package = ['GS', ['AR', ['RE', self.EID]]]
				self.Networking.gpsnet.send(package)
				print("Remove (nanoshooter) Entity request sent via Networking.gpsnet.send(request)...")
	
	def aimControl(self):
		pos = self.mouseOver.hitPosition
		self.aimPoint.position = pos
	
	def getDesiredLocalMovement(self):
		Controller = self.Interface.Inputs.Controller
		
		SPEED = 200.0
		MOD = 1.0
		
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


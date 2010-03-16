### Nanoshooter Entity ###

class Class:
	def __init__(self, EID, LocalGame):
		self.type = "nanoshooter"
		self.EID = EID
		
		self.LocalGame = LocalGame
		self.Admin = LocalGame.Admin
		self.GameState = LocalGame.GameState
		self.Networking = LocalGame.Networking
		self.Interface = LocalGame.Interface
		
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
	
	
	def getDescription(self):
		return self.GameState.getEntity(self.EID)
	
	def getOwner(self):
		return self.getDescription()['O']
	
	def getController(self):
		return self.getDescription()['C']
	
	################################################
	################################################
	################################################
	################################################
	
	def run(self):
		UID = self.Admin.getUID()
		
		if self.getOwner() == UID: self.ownerDataSimulate()
		else: self.ownerDataReplicate()
		
		if self.getController() == UID: self.controllerDataSimulate()
		else: self.controllerDataReplicate()
	
	################################################
	################################################
	################################################
	################################################
	
	
	def ownerDataSimulate(self):
		"""
		Simulates owner data, and updates the changes to the GameState via Networking.
		"""
		pass
	
	def ownerDataReplicate(self):
		"""
		Replicates the GameState description of this entity's owner data.
		"""
		pass
	
	################################################
	################################################
	################################################
	################################################
	
	
	def controllerDataSimulate(self):
		"""
		Simulates controller data, and updates the changes to the GameState via Networking.
		"""
		# Camera Management
		self.LocalGame.Camera.set(self.cam)
		self.suicideControlLoop()
		self.displayAimPoint()
		self.trackToAimPoint()
		
		# Movement can only occur when the terminal is not active.
		if not self.Interface.Terminal.active:
			X, Y, Z = self.getDesiredLocalMovement()
			self.gameObject.applyForce( (X,Y,Z), 0 )
			self.Resources.Tools.Damper.dampXY(self.gameObject, 20.0)
	
	def controllerDataReplicate(self):
		"""
		Replicates the GameState description of this entity's controller data to the local self's copy.
		"""
		pass
	
	
	################################################
	################################################
	################################################
	################################################
	
	def end(self):
		self.LocalGame.Camera.clear()
		self.aimPoint.endObject()
		self.aimPoint = None
		self.gameObject.endObject()
		self.gameObject = None
		print("Nanoshooter Entity Ended.")
	
	def suicideControlLoop(self):
		if not self.Interface.Terminal.active:
			suicideStatus = self.Interface.Inputs.Controller.getStatus("suicide")
			if suicideStatus == 1:
				# Suicide!
				package = ['GS', ['AR', ['RE', self.EID]]]
				self.Networking.gpsnet.send(package)
				print("Remove (nanoshooter) Entity request sent via Networking.gpsnet.send(request)...")
	
	def displayAimPoint(self):
		pos = self.mouseOver.hitPosition
		if pos[0] or pos[1] or pos[2]:
			self.aimPoint.position = pos
		else:
			self.aimPoint.position = [0.0, 0.0, -100.0]
	
	def trackToAimPoint(self):
		pos = self.mouseOver.hitPosition
		
		if pos[0] or pos[1] or pos[2]:
			pos[2] = self.gameObject.position[2]
			self.trackTo(pos)
	
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
	
	def trackTo(self, point):
		import Mathutils
		
		# Getting the offset (position of point relative to gameObject)
		oX = point[0] - self.gameObject.position[0]
		oY = point[1] - self.gameObject.position[1]
		oZ = point[2] - self.gameObject.position[2]
		
		# Getting the Y Vector of our Orientation Matrix
		Y = Mathutils.Vector([oX, oY, oZ])
		Y.normalize()
		
		# Creating the Z Vector (facing up)
		Z = Mathutils.Vector([0.0, 0.0, 1.0])
		
		# Generating the X Vector (cross product of Y and Z)
		X = Y.cross(Z)
		
		# Creating our Orientation
		ori1 = [X[0], Y[0], Z[0]]
		ori2 = [X[1], Y[1], Z[1]]
		ori3 = [X[2], Y[2], Z[2]]
		
		ori = [ori1, ori2, ori3]
		
		# Applying the new orientation to the gameObject
		self.gameObject.orientation = ori


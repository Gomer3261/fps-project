### Nanoshooter ###
import base_entity

class Class(base_entity.Class):
	type = "nanoshooter"
	
	def initiateGameStateData(self):
		"""
		Initiates the GameState OwnerData and ControllerData for this entity.
		"""
		import time
		
		OD = self.getOD()
		OD['HP'] = 100
		
		CD = {}
		CD['P'] = [0.0, 0.0, 0.0] # Position
		CD['AP'] = [0.0, 0.0, 0.0] # AimPoint
		CD['S'] = 0 # Shoots fired by controller
		
		self.sendData('OD', None, OD)
		self.sendData('CD', None, CD)
	
	
	
	def initiate(self):
		try: ARGS = self.getOD()['ARGS']
		except: ARGS = {}
		
		self.fireRate = 2.0 # Shots per second...
		self.damage = 51 # Damage per shot...
		
		self.updateClock = self.CLOCK()
		self.fireRateClock = self.CLOCK()
		
		self.targetPosition = [0.0, 0.0, 0.0] # These are used for
		self.targetAimPoint = [0.0, 0.0, 0.0] # Interpolation.
		
		# Local CD
		self.shotsFired = 0 # Local copy of number of shots fired
		if 'S' in ARGS: self.shotsFired = ARGS['S']
		
		# Local OD
		self.HP = 100
		self.lastHP = self.HP
		self.lastDamageFrom = 0 # UID responsible for last damage
		
		import GameLogic as gl
		own = gl.getCurrentController().owner
		
		# Initiating the gameObject
		self.gameObject = gl.getCurrentScene().addObject("nanoshooter", own)
		self.gameObject['EID'] = self.EID
		self.gameObject['damageable'] = True
		
		# Starting Position
		if self.weAreController():
			self.gameObject.position = ARGS['P']
		
		# Initiating the Aimpoint
		self.aimPoint = gl.getCurrentScene().addObject("ns_aimPoint", own)
		
		# If we are not the controller, the aimpoint is not visible.
		if not self.weAreController():
			self.aimPoint.visible = False
		
		self.gameObject['dyn'] = True
		
		# Getting the Controller
		self.cont = self.gameObject.controllers[0]
		# Getting the Sensors
		self.mouseOver = self.cont.sensors["mouseOver"]
		# Getting the Camera
		self.cam = self.cont.actuators["cam"].owner
		
		#print("Nanoshooter Initiated.")
	
	def end(self):
		self.LocalGame.Camera.clear()
		self.aimPoint.endObject()
		self.aimPoint = None
		self.gameObject.endObject()
		self.gameObject = None
		#print("Nanoshooter Entity Ended.")
	
	def handleMemos(self):
		for memo in self.memos:
			memoFlag, memoData = memo
			if memoFlag == 'DMG':
				damage, responsibleUID = memoData
				self.HP -= damage
				self.lastDamageFrom = responsibleUID
		self.memos = []
	
	################################################
	################################################
	################################################
	################################################
	
	
	def ownerDataSimulate(self):
		"""
		Simulates owner data, and updates the changes to the GameState via Network.
		"""
		self.handleMemos()
		# Delete this entity when we run out of health?
		if (self.HP <= 0) and not (self.lastHP <= 0):
			self.Network.send( ('GS', ('AR', ('RE', self.EID))) )
			ourName = self.GameState.getUserName(self.getController())
			killerName = self.GameState.getUserName(self.lastDamageFrom)
			print(self.Admin.UID, ourName, self.lastDamageFrom, killerName)
			self.Network.sendText( 0,"%s killed %s."%(killerName, ourName) )
		OD = self.getOD()
		if OD['HP'] != self.HP:
			OD['HP'] = self.HP
			self.throwData('OD', None, OD)
		self.lastHP = self.HP
	
	def ownerDataReplicate(self):
		"""
		Replicates the GameState description of this entity's owner data.
		"""
		OD = self.getOD()
		self.HP = OD['HP']
	
	################################################
	################################################
	################################################
	################################################
	
	
	def controllerDataSimulate(self):
		"""
		Simulates controller data, and updates the changes to the GameState via Network.
		"""
		# Camera Management
		self.LocalGame.Camera.set(self.cam)
		self.suicideControlLoop()
		self.displayAimPoint()
		self.trackToAimPoint()
		
		CD = self.getCD()
		OD = self.getOD()
		
		# Movement can only occur when the terminal is not active.
		if not self.Interface.Terminal.active:
			X, Y, Z = self.getDesiredLocalMovement()
			self.gameObject.applyForce( (X,Y,Z), 0 )
			self.Resources.Tools.Damper.dampXY(self.gameObject, 20.0)
		
		if self.Interface.Inputs.Controller.getStatus("use") == 1:
			if self.fireRateClock.get() > (1.0/self.fireRate):
				self.fireForEffect()
				self.shoot(damage=self.damage)
				self.shotsFired += 1
				self.fireRateClock.reset()
		
		if self.updateClock.get() > 0.1:
			CD['P'] = self.gameObject.position
			CD['AP'] = self.aimPoint.position
			CD['S'] = self.shotsFired
			self.throwData('CD', None, CD)
			self.updateClock.reset()
	
	def controllerDataReplicate(self):
		"""
		Replicates the GameState description of this entity's controller data to the local self's copy.
		"""
		shotsWeNeedToFire = 0
		try:
			CD = self.getCD()
			self.targetPosition = CD['P']
			self.targetAimPoint = CD['AP']
			shotsWeNeedToFire = CD['S'] - self.shotsFired
		except: pass
		self.gameObject.position = self.interpolate(self.gameObject.position, self.targetPosition, 15.0)
		self.aimPoint.position = self.interpolate(self.aimPoint.position, self.targetAimPoint, 15.0)
		self.trackToAimPoint()
		if shotsWeNeedToFire > 0:
			if self.fireRateClock.get() > (1.0/self.fireRate):
				self.fireForEffect()
				self.shotsFired += 1
				self.fireRateClock.reset()

	################################################
	################################################
	################################################
	################################################
	
	def fireForEffect(self, range=500.0):
		import Rasterizer
		projectedPoint = self.getProjectedPoint(range)
		obj, point, normal = self.gameObject.rayCast(projectedPoint, self.gameObject.position)
		if point:
			Rasterizer.drawLine(self.gameObject.position, point, [1.0, 0.5, 0.0])
		else:
			Rasterizer.drawLine(self.gameObject.position, projectedPoint, [1.0, 0.5, 0.0])
	
	def shoot(self, range=500.0, damage=10):
		import Rasterizer
		projectedPoint = self.getProjectedPoint(range)
		obj, point, normal = self.gameObject.rayCast(projectedPoint, self.gameObject.position)
		if obj:
			if "damageable" in obj:
				EID = obj['EID']
				self.sendMemo( EID, ("DMG", (damage, self.Admin.UID)) )
				#print('NS: Damage memo sent to: %s'%EID)
	
	def getProjectedPoint(self, distance):
		o = self.gameObject.orientation
		Yp = [ o[0][1], o[1][1], o[2][1] ]
		return self.multiplyPosition(Yp, distance)
	
	def multiplyPosition(self, p, x):
		return [ p[0]*x, p[1]*x, p[2]*x ]
	
	def interpolate(self, origin, target, percent=20.0):
		"""
		Interpolates two positions by a percentage; used for smoothing motion between
		positional updates.
		"""
		oX, oY, oZ = origin
		tX, tY, tZ = target
		
		dX = tX - oX # Getting the difference between them
		dY = tY - oY
		dZ = tZ - oZ
		
		fX = dX*(percent/100.0) # Getting a fraction of the difference
		fY = dY*(percent/100.0)
		fZ = dZ*(percent/100.0)
		
		nX = oX + fX # Applying the fraction of difference to the origin
		nY = oY + fY
		nZ = oZ + fZ
		
		result = [nX, nY, nZ]
		return result
	
	def suicideControlLoop(self):
		if not self.Interface.Terminal.active:
			suicideStatus = self.Interface.Inputs.Controller.getStatus("suicide")
			if suicideStatus == 3:
				self.sendMemo(self.GameState.getDirectorEID(), ('RE', self.EID))
	
	def displayAimPoint(self):
		pos = self.mouseOver.hitPosition
		if pos[0] or pos[1] or pos[2]:
			self.aimPoint.position = pos
		else:
			self.aimPoint.position = [0.0, 0.0, -100.0]
	
	def trackToAimPoint(self):
		X, Y, Z = self.aimPoint.position
		if X or Y:
			Z = self.gameObject.position[2]
			self.trackTo([X, Y, Z])
	
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


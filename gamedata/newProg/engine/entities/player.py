# PLAYER ENTITY
import engine.entities.baseEntity as baseEntity
class Class(baseEntity.Class):



	def initializeGamestateData(self, gamestate):
		data = {}
		data['H'] = 100	# Health Integer
		data['P'] = [0.0, 0.0, -100.0] # Position
		data['R'] = [0.0, 1.0, 0.0] # Aim Location
		data['F'] = False # Firing Status
		data['S'] = 1 # Stance. 1=stand, 2=crouch, 3=prone
		
		delta = {'E':{self.id:data}} # Putting it in gamestate.delta form
		gamestate.mergeDelta(delta) # merging it with gamestate's delta
	
	def initialize(self, gamestate):
		
		if self.control:
			self.lastUpdate = self.time.time()
			self.updateInterval = 0.1 # every tenth of a second.
			
			self.mass = 80.0
			self.speedForce = 80.0*self.mass # Speed in force of general player movement
			self.sprintMod = 1.75 # Speed multiplier when sprinting (1.0=no change, 2.0=double)
			self.crouchMod = 0.5 # Speed multiplier when crouching (sprint effects crouching speed as well)
			self.jumpForce = 250.0*self.mass # Upward force when jump is executed.
			self.slopeInfluence = 0.8 # The power of slope damping. 1.0 is pretty powerful, 2.0 makes it impossible to go up steep slopes, 0.5 makes it slight but noticeable.
			self.noTouchMod = 0.02 # The modifier on desired movement when the player is not touching the ground.
			
			self.firing = False
			self.stance = 1 # 1=stand, 2=crouch, 3=prone
			
			import bge
			self.object = bge.logic.getCurrentScene().addObject("player", bge.logic.getCurrentController().owner)
			self.object["id"] = self.id
			self.aimpoint = bge.logic.getCurrentScene().addObject("player_aimpoint", bge.logic.getCurrentController().owner)
			self.aimpoint.worldPosition = (0,0,5)
			
			self.aim = self.object.children['player_aim']
			self.camera = self.aim.children['player_camera']
			
			self.floorSensors = []
			self.floorSensors.append( self.object.children['player_floorSensor0'] )
			self.floorSensors.append( self.object.children['player_floorSensor1'] )
			self.floorSensors.append( self.object.children['player_floorSensor2'] )
			self.floorSensors.append( self.object.children['player_floorSensor3'] )
			self.floorSensors.append( self.object.children['player_floorSensor4'] )
			
			self.ceilingRays = []
			self.ceilingRays.append( self.object.children['player_ceilingSensor0'] )
			self.ceilingRays.append( self.object.children['player_ceilingSensor1'] )
			self.ceilingRays.append( self.object.children['player_ceilingSensor2'] )
			self.ceilingRays.append( self.object.children['player_ceilingSensor3'] )
			self.ceilingRays.append( self.object.children['player_ceilingSensor4'] )
			
			self.engine.interface.mouse.reset()
			self.angle_y = 0.0
		else:
			import bge
			self.object = bge.logic.getCurrentScene().addObject("player_proxy", bge.logic.getCurrentController().owner)
			self.targetPosition = [0.0, 0.0, -100.0]
	
	def end(self):
		self.engine.camera.reset()
		self.object.endObject()
		self.aimpoint.endObject()
	
	
	
	
	
	
	
	
	
	##################
	###### HOST ###### Server-side behaviour for this entity.
	################## Defines server-data; handles memos.
	def host(self, gamestate):
		pass
	
	####################
	###### CLIENT ###### Client-side behaviour for this entity.
	#################### Replicates server-data.
	def client(self, gamestate):
		pass
	
	########################
	###### CONTROLLER ###### Controller behaviour for this entity.
	######################## Defines controller-data; creates memos.
	def controller(self, gamestate):
		self.engine.camera.offer(self.camera, 10)
		
		self.doPlayerMovement()
		if not self.engine.interface.mouse.reserved: self.doMouseLook()
		
		hitEntityId, aimPosition = self.doAim()
		if aimPosition:
			self.aimpoint.worldPosition=aimPosition
			self.aimpoint.visible = True
		else:
			self.aimpoint.visible = False
		
		if self.time.time()-self.lastUpdate > self.updateInterval:
			pos = [0.0, 0.0, 0.0]
			for i in range(3): pos[i]=str(round(self.object.worldPosition[i], 3))
			self.submitDelta( {'E': {self.id:{'P':pos}} } )
			self.lastUpdate = self.time.time()
		
		if self.engine.interface.isControlPositive('suicide'):
			self.submitDelta( {'E':{self.id:None}} )
			
	###################
	###### PROXY ###### Proxy behaviour for this entity.
	################### Replicates controller-data.
	def proxy(self, gamestate):
		data = self.engine.gamestate.getById(self.id)
		if 'P' in data:
			pos = data['P']
			for i in range(3): pos[i]=float(pos[i])
			self.targetPosition = pos
		self.object.worldPosition = self.interpolate(self.object.worldPosition, self.targetPosition, 20.0)
	
	
	
	
	
	
	
	
	def doAim(self):
		"""
		Project a ray from self.aim's Y axis.
		We will
		return hitEntityId, aimposition
		"""
		dir = self.camera.worldOrientation[2]
		hitdata = self.camera.rayCast([dir[0]*-10000, dir[1]*-10000, dir[2]*-10000], [self.camera.worldPosition[0], self.camera.worldPosition[1], self.camera.worldPosition[2]], 10000)
		if hitdata[0] and "id" in hitdata[0]:
			return hitdata[0]["id"], hitdata[1]
		return None, hitdata[1]
	
	def doPlayerMovement(self):
		movement = self.getDesiredMovement()
		movement = self.applySprint(movement)
		movement = self.applyStance(movement)
		#movement = self.doSlopeDamping(movement)
		movement = self.degradeMovementWhenNotOnGround(movement)
		if not self.engine.interface.terminalIsActive(): self.object.applyForce(movement, 1)
		self.doDamping()
	
	def getDesiredMovement(self):
		import engine.interface as interface
		X=0.0; Y=0.0; Z=0.0
		if interface.isControlPositive('forward'): Y+=self.speedForce
		if interface.isControlPositive('backward'): Y-=self.speedForce
		if interface.isControlPositive('left'): X-=self.speedForce
		if interface.isControlPositive('right'): X+=self.speedForce
		if X and Y: X *= 0.7071; Y *= 0.7071
		if (interface.getControlStatus('jump') == 1) and self.isOnGround(): Z=self.jumpForce
		return [X, Y, Z]
	
	def applySprint(self, movement):
		import engine.interface as interface
		newMovement = movement[:] # Making a copy, not a reference
		if interface.isControlPositive("sprint"):
			for i in range(2): # We're only doing the first two, X and Y.
				newMovement[i] = movement[i] * self.sprintMod
		return newMovement

	def applyStance(self, movement):
		newMovement = movement[:]
		if self.stance == 2: # stance 2 is crouch
			for i in range(2):
				newMovement[i] = movement[i] * self.crouchMod
		return newMovement

	def degradeMovementWhenNotOnGround(self, movement):
		if self.isOnGround(): return movement
		else:
			for i in range(3): movement[i] *= self.noTouchMod
			return movement
	
	def doDamping(self):
		d=1.0
		if self.isOnGround(): d=25.0*self.mass
		x,y,z=self.object.getVelocity()
		x*=-d; y*=-d
		self.object.applyForce([x, y, 0.0], 0)

	def isOnGround(self):
		for floorSensor in self.floorSensors:
			pos = (floorSensor.worldPosition[0], floorSensor.worldPosition[1], floorSensor.worldPosition[2] - 0.2)
			if floorSensor.rayCastTo(pos, 0.2): return True
		return False
	
	def interpolate(self, origin, target, percent=20.0): # Interpolates positions by a percentage.
		oX,oY,oZ=origin; tX,tY,tZ=target
		# Getting the difference between them
		dX=tX-oX; dY=tY-oY; dZ=tZ-oZ
		# Getting a fraction of the difference
		fX=dX*(percent/100.0); fY=dY*(percent/100.0); fZ=dZ*(percent/100.0)
		# Applying the fraction of difference to the origin
		nX=oX+fX; nY=oY+fY; nZ=oZ+fZ
		return [nX, nY, nZ]

	def doMouseLook(self):
		"""
		A mouse script uses movement of the mouse to cause object rotation.
		"""
		import engine
		mouse = engine.interface.mouse
		if mouse.isPositive():
			rotation = [0, 0]
			rotation[0], rotation[1] = mouse.getPositionFromCenter()
			
			rotation[0] *= engine.interface.getSetting("mxsens")/1000
			self.object.applyRotation([0, 0, rotation[0]], 0)
			
			rotation[1] *= engine.interface.getSetting("mysens")/1000
			
			#limit of 90 degrees for the y axis
			if self.angle_y+rotation[1] <= -1.5706:
				rotation[1] = -1.5706-self.angle_y
			if self.angle_y+rotation[1] >= 1.5706:
				rotation[1] = 1.5706-self.angle_y
		
			self.angle_y += rotation[1]
			self.camera.applyRotation([rotation[1], 0, 0], 1)
			
			mouse.reset()

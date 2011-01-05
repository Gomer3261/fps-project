# PLAYER ENTITY
import engine.entities.baseEntity as baseEntity
class Class(baseEntity.Class):
	def initializeGamestateData(self, gamestate):
		data = {}
		data['H'] = 100	# Health Integer
		data['P'] = [0.0, 0.0, -100.0] # Position
		data['R'] = [0.0, 1.0, 0.0] # Aim Location
		data['F'] = False # Firing Status
		data['S'] = 1 # Stance 1=stand, 2=crouch, 3=prone
		
		delta = {'E':{self.id:data}} # Putting it in gamestate.delta form
		gamestate.mergeDelta(delta) # merging it with gamestate's delta
	
	def initialize(self, gamestate):
		
		if self.control:
			self.speedForce = 80.0 # Speed in force of general player movement
			self.sprintMod = 1.75 # Speed multiplier when sprinting (1.0=no change, 2.0=double)
			self.crouchMod = 0.5 # Speed multiplier when crouching (sprint effects crouching speed as well)
			self.jumpForce = 250.0 # Upward force when jump is executed.
			self.slopeInfluence = 0.8 # The power of slope damping. 1.0 is pretty powerful, 2.0 makes it impossible to go up steep slopes, 0.5 makes it slight but noticeable.
			self.noTouchMod = 0.02 # The modifier on desired movement when the player is not touching the ground.
			
			import bge
			self.object = bge.logic.getCurrentScene().addObject("player", bge.logic.getCurrentController().owner)
			
			self.camera = self.object.children['player_camera']
			
			self.floorSensor = []
			self.floorSensor.append( self.object.children['player_floorSensor0'] )
			self.floorSensor.append( self.object.children['player_floorSensor1'] )
			self.floorSensor.append( self.object.children['player_floorSensor2'] )
			self.floorSensor.append( self.object.children['player_floorSensor3'] )
			self.floorSensor.append( self.object.children['player_floorSensor4'] )
			
			self.ceilingRays = []
			self.ceilingRays.append( self.object.children['player_ceilingSensor0'] )
			self.ceilingRays.append( self.object.children['player_ceilingSensor1'] )
			self.ceilingRays.append( self.object.children['player_ceilingSensor2'] )
			self.ceilingRays.append( self.object.children['player_ceilingSensor3'] )
			self.ceilingRays.append( self.object.children['player_ceilingSensor4'] )
		else:
			import bge
			self.object = bge.logic.getCurrentScene().addObject("player_proxy", bge.logic.getCurrentController().owner)
	
	def end(self):
		self.engine.camera.reset()
		self.object.endObject()
	
	
	
	def serverDataSimulate(self, gamestate):
		"""
		Simulates stuff, and returns gamestate delta data to the
		mainloop, where it is merged with the gamestate delta.
		Memos are handled by this method.
		"""
		# Handle memos before clearing them each run.
		self.memos = [] # Clear memos when you're done with them.
		return [] # Return delta data to be merged with gamestate.delta
	
	def serverDataReplicate(self, gamestate):
		"""
		This is where memos are born. Memos are messages to serverside entities.
		"""
		memos = []
		id=None; data=None
		memo=(id,data)
		return memos # memos are used when you shoot people.
	
	def controllerDataSimulate(self, gamestate):
		"""
		Simulates stuff, and returns gamestate delta data to the
		mainloop, where it is merged with the gamestate delta.
		"""
		deltas = []
		if self.engine.interface.isControlPositive('suicide'): deltas.append( {'E':{self.id:None}} )
		self.engine.camera.offer(self.camera, 10)
		return deltas # Return delta data to be merged with gamestate.delta
	
	def controllerDataReplicate(self, gamestate):
		pass
	
	
	
	
	
	
	
	
	def doPlayerMovement(self):
		import engine.interface as interface
		movement = self.getDesiredMovement()
		movement = self.applySprint(movement)
		movement = self.applyStance(movement)
		#movement = self.doSlopeDamping(movement)
		movement = self.degradeMovementWhenNotOnGround(movement)
		if interface.terminalIsActive(): self.object.applyForce(movement, 1)
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
		if self.isOnGround(): d=25.0
		x,y,z=obj.getVelocity()
		x*=-d; y*=-d
		obj.applyForce([x, y, 0.0], 0)





	def isOnGround(self):
		for sensor in self.floorSensors:
			if sensor.positive: return True
		return False


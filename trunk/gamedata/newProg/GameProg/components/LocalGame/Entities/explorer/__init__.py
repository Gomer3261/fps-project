### Explorer Entity ###
import base_entity
class Class(base_entity.Class):
	type = "explorer"
	
	def initiate(self):
		self.gameObject = None
		self.selectedEntityType = ""
		self.selectedEntityGhost = None
		self.entityRotationStep = 0
		self.entityRotationAngles = [[0.0, 1.0, 0.0], [0.7071, 0.7071, 0.0], [1.0, 0.0, 0.0], [0.7071, -0.7071, 0.0], [0.0, -1.0, 0.0], [-0.7071, -0.7071, 0.0], [-1.0, 0.0, 0.0], [-0.7071, 0.7071, 0.0]]
		self.aimedEID = 0
		
		if self.weAreController():
			# Initiating the gameObject
			import bge
			own = bge.logic.getCurrentController().owner
			self.gameObject = bge.logic.getCurrentScene().addObject("explorer", own)
			
			self.aimEnd = self.gameObject.controllers[0].actuators["aimEnd"].owner
			
			# Getting the Camera
			self.cam = self.gameObject.controllers[0].actuators["cam"].owner
			
			# The gameObject acts as both the XPivot and the YPivot for the explorer.
			self.XPivot = self.gameObject
			self.YPivot = self.gameObject
			
			self.Interface.out("Explorer Initiated.", terminal=False, console=True)
	
	def end(self):
		self.LocalGame.Camera.clear()
		if self.gameObject:
			self.gameObject.endObject()
			self.gameObject = None
		self.clearGhost()
		self.Interface.out("Explorer Ended.", terminal=False, console=True)
	
	def run(self):
		if self.weAreController():
			# Camera Management
			self.LocalGame.Camera.set(self.cam)
			self.doMouseLook()
			
			self.handleSelection()
			aimpoint = self.getAimpoint()
			self.handleGhostRotation()
			self.handleGhostDisplay(aimpoint)
			self.handleEntityPlacement(aimpoint)
			self.handleEntityRemoval()
			
			
			self.suicideControlLoop()
			
			# Movement can only occur when the terminal is not active.
			if not self.Interface.Terminal.active:
				X, Y, Z = self.getDesiredLocalMovement()
				self.gameObject.applyMovement( (X,Y,0), 1 ) # X and Y applied locally.
				self.gameObject.applyMovement( (0,0,Z), 0 ) # Z applied globally.
	
	#######################################################
	#######################################################
	#######################################################
	
	def handleSelection(self):
		Controller = self.Interface.Inputs.Controller
		if Controller.getStatus("select-spawnpoint") == 3:
			if self.selectedEntityType != "spawnpoint":
				self.clearGhost()
				self.selectedEntityType = "spawnpoint"
			else:
				self.selectedEntityType = ""
		if Controller.getStatus("select-box") == 3:
			if self.selectedEntityType != "box":
				self.clearGhost()
				self.selectedEntityType = "box"
			else:
				self.selectedEntityType = ""
	
	def increaseRotationStep(self):
		if self.entityRotationStep != (len(self.entityRotationAngles)-1):
			self.entityRotationStep += 1
		else:
			self.entityRotationStep = 0
	
	def handleGhostRotation(self):
		Controller = self.Interface.Inputs.Controller
		if Controller.getStatus("rotate-entity") == 3:
			self.increaseRotationStep()
	
	def clearGhost(self):
		if self.selectedEntityGhost:
			self.selectedEntityGhost.endObject()
			self.selectedEntityGhost = None
	
	def handleGhostDisplay(self, aimpoint):
		if self.selectedEntityType:
			if not self.selectedEntityGhost:
				import bge
				self.selectedEntityGhost = bge.logic.getCurrentScene().addObject(self.selectedEntityType+"_ghost", bge.logic.getCurrentController().owner)
				self.selectedEntityGhost.position = self.getEntitySpawnHeight(aimpoint)
				self.selectedEntityGhost.alignAxisToVect(self.entityRotationAngles[self.entityRotationStep], 1)
				self.selectedEntityGhost.alignAxisToVect([0.0, 0.0, 1.0], 2)
			else:
				self.selectedEntityGhost.position = self.getEntitySpawnHeight(aimpoint)
				self.selectedEntityGhost.alignAxisToVect(self.entityRotationAngles[self.entityRotationStep], 1)
				self.selectedEntityGhost.alignAxisToVect([0.0, 0.0, 1.0], 2)
		else:
			if self.selectedEntityGhost:
				self.clearGhost()
	
	def getEntitySpawnHeight(self, aimpoint):
		return [aimpoint[0], aimpoint[1], aimpoint[2]+(self.selectedEntityGhost['height']/2.0)]
	
	def handleEntityPlacement(self, aimpoint):
		Controller = self.Interface.Inputs.Controller
		if Controller.getStatus("add-entity") == 3:
			if self.selectedEntityType:
				if self.LocalGame.getEntityClass(self.selectedEntityType):
					UIDs = self.Admin.getHostUID(), self.Admin.getHostUID()
					args = {"P":self.getEntitySpawnHeight(aimpoint), "R":self.entityRotationAngles[self.entityRotationStep]}
					self.Network.send( ('GS', ('AR', ('SE', (self.selectedEntityType, UIDs, args)))) )
	
	def handleEntityRemoval(self):
		Controller = self.Interface.Inputs.Controller
		if Controller.getStatus("remove-entity") == 3:
			EID = self.getHitEID()
			if EID:
				self.Network.send( ('GS', ('AR', ('RE', EID))) )
	
	def getAimpoint(self):
		start = self.gameObject.position
		target = self.aimEnd.position
		#import bge; bge.render.drawLine(start, target, [1.0, 0.0, 0.0])
		obj, point, normal = self.gameObject.rayCast(target, start)
		if point: target = point
		return target
	
	def getHitEID(self):
		start = self.gameObject.position
		target = self.aimEnd.position
		#import bge; bge.render.drawLine(start, target, [1.0, 0.0, 0.0])
		obj, point, normal = self.gameObject.rayCast(target, start)
		if obj:
			if "EID" in obj:
				entity = self.GameState.getEntity(obj["EID"])
				if entity:
					print(obj['EID'])
					return obj['EID']
		return None
		
	#######################################################
	#######################################################
	#######################################################
	
	def suicideControlLoop(self):
		if not self.Interface.Terminal.active:
			suicideStatus = self.Interface.Inputs.Controller.getStatus("suicide")
			if suicideStatus == 3:
				self.sendMemo(self.GameState.getDirectorEID(), ('RE', self.EID))
	
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

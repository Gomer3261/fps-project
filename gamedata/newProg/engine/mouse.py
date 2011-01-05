##############################
### ------	MOUSE	------ ###
##############################
# For getting Mouse movement information.

class createMouse:
	def __init__(self):
		import engine; self.engine=engine
		import bge; self.bge=bge
		self.step=0
		self.width=self.bge.render.getWindowWidth()
		self.height=self.bge.render.getWindowHeight()
		self.centerX=self.width//2
		self.centerY=self.height//2
	def reset(self): self.bge.logic.mouse.position = (0.5, 0.5) # Resets the mouse back to the center of the screen.
	def show(self, vis=True): self.bge.logic.mouse.visible = vis # Shows the mouse cursor.
	def hide(self, vis=False): self.bge.logic.mouse.visible = vis # Hides the mouse cursor.
	def isPositive(self): return (self.bge.logic.mouse.events[self.bge.events.MOUSEX] or self.bge.logic.mouse.events[self.bge.events.MOUSEY])
	def getPosition(self): # Gets the current mouse position in pixels.
		x,y=self.bge.logic.mouse.position
		x*=self.width; y*=self.height
		import math
		x=math.floor(x)
		y=math.floor(y)
		return x,y
	def getPositionFromCenter(self):
		x,y=self.getPosition()
		x-=self.centerX; y-=self.centerY
		return x,y
	def getMovement(self):
		x,y=self.getPositionFromCenter()
		if self.step>2: self.reset(); self.step=0
		self.step+=1
		return x,y
		
	
	
	def doMouseLook(self, xPivot, yPivot, sens=(5.0,5.0), inverts=(False,False), restrictY=False):
		mxsens,mysens=sens; invertX,invertY=inverts
		X,Y = self.getMovement(); x,y=X,Y
		x*=-mxsens*0.001; y*=-mysens*0.001
		if invertX: x*=-1
		if invertY: y*=-1
		
		isMovingUp= (Y>=0.0)
		ori = yPivot.orientation
		ZZ=ori[2][2]; isUpright=(ZZ>=0.0)
		YZ=ori[2][1]; isFacingUp=(YZ>=0.0)
		
		if not isUpright: xPivot.applyRotation([0,0,-x], 0)
		else: xPivot.applyRotation([0,0,x],0)
		
		#xPivot.applyRotation([0, 0, x], 0)
		yPivot.applyRotation([y, 0, 0], 1)
		
		#if restrictY:
		#	if isUpright: yPivot.applyRotation([y, 0, 0], 1)
		#	elif isMovingUp and (not isFacingUp): yPivot.applyRotation([y, 0, 0], 1)
		#	elif (not isMovingUp) and isFacingUp: yPivot.applyRotation([y, 0, 0], 1)
		#else: yPivot.applyRotation([y, 0, 0], 1)

object = createMouse()
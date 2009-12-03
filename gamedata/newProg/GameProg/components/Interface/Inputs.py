############################
### ------ inputs ------ ###
############################
### Copyright 2009 Chase Moskal

class Class:
	controller = None




	#initiates the module
	def __init__(self):
		"""Init the module."""
		
		#creating the inputs object (for sensors)
		import GameLogic as gl
		BaseObject = gl.getCurrentController().owner
		self.inputsObject = gl.getCurrentScene().addObject("GP_Inputs", BaseObject)
		con = self.inputsObject.controllers[0]
		
		self.Controller = None
		self.Controller = self.CONTROLLER(con)
		
		self.Mouse = self.MOUSE(con)
		
		print("Inputs Initiated")
	
	
	
	
	
	
	
	
	##############################
	### ------	MOUSE	------ ###
	##############################
	# For getting Mouse movement information.

	class MOUSE:
		import math
		import Rasterizer

		def __init__(self, cont):
			self.cont = cont
			self.mousemove = cont.sensors["mousemove"]

			self.width = self.Rasterizer.getWindowWidth()
			self.height = self.Rasterizer.getWindowHeight()

			self.centerX = self.width/2
			self.centerY = self.height/2


		def reset(self):
			self.Rasterizer.setMousePosition(self.centerX, self.centerY)


		def show(self, vis=1):
			self.Rasterizer.showMouse(vis)

		def hide(self, vis=0):
			self.Rasterizer.showMouse(vis)

		def getPosition(self):
			position = self.mousemove.position

			X = position[0]
			Y = position[1]

			return X, Y


		def isAtCenter(self):
			X, Y = self.getPosition()
			center = 1

			if X != self.centerX:
				center = 0

			if Y != self.centerY:
				center = 0

			return center


		def getPositionFromCenter(self):
			X, Y = self.getPosition()

			X = (X-self.centerX)
			Y = (self.centerY-Y)

			return X, Y

		def isPositive(self):
			if self.mousemove.positive:
				return 1
			else:
				return 0

		def getMovement(self):
			if self.isPositive():
				X, Y = self.getPositionFromCenter()
			else:
				X = 0
				Y = 0
			if X or Y:
				self.reset()
			return X, Y











	################################
	### ------ CONTROLLER ------ ###
	################################
	#This object is used to check the values of players custom controls.

	class CONTROLLER:
		events = {}

		keyboard = None
		
		other = {}
		
		other["LMB"] = None
		other["RMB"] = None
		other["MMB"] = None

		other["MWU"] = None
		other["MWD"] = None

		

		def __init__(self, con):

			#finding sensors
			KEYBOARD = con.sensors["KEYBOARD"]
			
			LMB = con.sensors["LMB"]
			RMB = con.sensors["RMB"]
			MMB = con.sensors["MMB"]

			MWU = con.sensors["MWU"]
			MWD = con.sensors["MWD"]
			
			###

			#setting variables.=
			self.keyboard = KEYBOARD
			
			self.other["LMB"] = LMB
			self.other["RMB"] = RMB
			self.other["MMB"] = MMB

			self.other["MWU"] = MWU
			self.other["MWD"] = MWD



			

		#Used to detect hit keys, and other control events. (1 control/event)
		class EVENT:
			def __init__(self, controller, control, value=None):
				self.controller = controller

				self.control = control
				self.getValue(value)
				
				self.kind = ""
				self.lastpositive = 0

				

			#converts the options value to a GameKeys value.
			def getValue(self, value=None):
				if not value:
					if control not in self.controller.controls:
						return None
					value = self.controller.controls[self.control]
					
				value = value.replace("-", "")
				value = value.upper()

				self.value = value

				return value

			

			#figures out the status of the event. (0 for inactive, 1 for just pressed, 2 for held, 3 for just released.)
			def getStatus(self):
				if self.value in self.controller.other:
					self.kind = "other"
					positive = self.controller.other[self.value].positive

					status = 0
					
					if positive:
						if self.lastpositive:
							status = 2 # being held
						else:
							status = 1 # just pressed
					else:
						if self.lastpositive:
							status = 3 # just released
						else:
							status = 0 # nothing

					self.lastpositive = positive
					return status
				
				else:
					self.kind = "key"
					import GameKeys
					status = self.controller.keyboard.getKeyStatus(getattr(GameKeys, self.value))
					return status

				

			#checks if the event is positive or not.
			def isPositive(self):
				status = self.getStatus()
				if (status == 1) or (status == 2):
					return 1
				return 0



		#checks for the event in self.events
		def getEvent(self, control):
			if control in self.events:
				event = self.events[control]
				return event
			else:
				return None

			

		#returns the status of the control. (0 for inactive, 1 for just pressed, 2 for held, 3 for just released.)
		def getStatus(self, control):
			event = self.getEvent(control)
			if not event:
				return None
			status = event.getStatus()
			return status

		

		#returns 1 if the control is positive.
		def isPositive(self, control):
			event = self.getEvent(control)
			if not event:
				return None
			positive = event.isPositive()
			return positive

		
		
		#changes the values of controls, and creates events to detect them.
		def setControls(self, controls):
			# controls is usually from options.py
			self.controls = {}
			self.events = {}
			
			self.controls = controls
			print "Controls set."

			for control in self.controls:
				value = self.controls[control]
				event = self.EVENT(self, control, value)
				self.events[control] = event
			#print "Events set."

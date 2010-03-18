############################
### ------ inputs ------ ###
############################
### Copyright 2009 Chase Moskal

class Class:


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
		
		print("  Interface/Input's happy.")
	
	
	
	
	##############################
	### ------	MOUSE	------ ###
	##############################
	# For getting Mouse movement information.

	class MOUSE:
		"""
		The Mouse class contains a set of functions that make working with the mouse easier.
		"""
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
			"""
			sets the mouse position to the center of the screen.
			"""
			self.Rasterizer.setMousePosition(self.centerX, self.centerY)


		def show(self, vis=1):
			"""
			makes the mouse visible.
			"""
			self.Rasterizer.showMouse(vis)

		def hide(self, vis=0):
			"""
			hides the mouse from view.
			"""
			self.Rasterizer.showMouse(vis)

		def getPosition(self):
			"""
			returns the position of the mouse. X, Y
			"""
			position = self.mousemove.position

			X = position[0]
			Y = position[1]

			return X, Y


		def isAtCenter(self):
			"""
			True if the mouse is in the center of the viewport.
			"""
			X, Y = self.getPosition()
			center = 1

			if X != self.centerX:
				center = 0

			if Y != self.centerY:
				center = 0

			return center


		def getPositionFromCenter(self):
			"""
			Returns the difference between the mouse position and the center of the screen. X, Y
			"""
			X, Y = self.getPosition()

			X = (X-self.centerX)
			Y = (self.centerY-Y)

			return X, Y

		def isPositive(self):
			"""
			True if mouse has moved.
			"""
			if self.mousemove.positive:
				return 1
			else:
				return 0

		def getMovement(self):
			"""
			Returns distance from the center of the screen. X, Y
			Resets mouse to center of the screen.
			"""
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

	class CONTROLLER:
		"""
		The Controller class is used to check the values of custom controls.
		"""
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



			

		class EVENT:
			"""
			The Event class is used to detect hit keys and other control related information. (1 control/event)
			"""
			def __init__(self, controller, control, value=None):
				self.controller = controller

				self.control = control
				self.getValue(value)
				
				self.kind = ""
				self.lastpositive = 0

				

			def getValue(self, value=None):
				"""
				converts the options value to a GameKeys value.
				"""
				if not value:
					if control not in self.controller.controls:
						return None
					value = self.controller.controls[self.control]
					
				value = value.replace("-", "")
				value = value.upper()

				self.value = value

				return value

			

			def getStatus(self):
				"""
				figures out the status of the event. (0 for inactive, 1 for just pressed, 2 for held, 3 for just released.)
				"""
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

				

			def isPositive(self):
				"""
				checks if the event is positive or not.
				"""
				status = self.getStatus()
				if (status == 1) or (status == 2):
					return 1
				return 0



		def getEvent(self, control):
			"""
			checks for the event in self.events
			"""
			if control in self.events:
				event = self.events[control]
				return event
			else:
				return None

			

		def getStatus(self, control):
			"""
			returns the status of the control. (0 for inactive, 1 for just pressed, 2 for held, 3 for just released.)
			"""
			event = self.getEvent(control)
			if not event:
				return None
			status = event.getStatus()
			return status

		

		def isPositive(self, control):
			"""
			returns 1 if the control is positive.
			"""
			event = self.getEvent(control)
			if not event:
				return None
			positive = event.isPositive()
			return positive

		
		
		def setControls(self, controls):
			"""
			changes the values of controls, and creates events to detect them.
			"""
			# controls are usually from options.py
			self.controls = {}
			self.events = {}
			
			self.controls = controls
			print "Interface/Inputs/Controller: Controls Set."

			for control in self.controls:
				value = self.controls[control]
				event = self.EVENT(self, control, value)
				self.events[control] = event
			#print "Events set."

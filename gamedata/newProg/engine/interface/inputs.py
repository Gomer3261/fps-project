 ############################
### ------ inputs ------ ###
############################
### Copyright 2009 Chase Moskal

class initializeInputs:


	#initiates the module
	def __init__(self):
		"""Init the module."""
		
		#creating the inputs object (for sensors)
		import bge
		
		self.controller = None
		self.controller = self.CONTROLLER()
		
		self.mouse = self.MOUSE()
	
	
	
	
	##############################
	### ------	MOUSE	------ ###
	##############################
	# For getting Mouse movement information.

	class MOUSE:
		"""
		The Mouse class contains a set of functions that make working with the mouse easier.
		"""
		import math
		import bge

		def __init__(self):

			self.width = self.bge.render.getWindowWidth()
			self.height = self.bge.render.getWindowHeight()

			self.centerX = self.width//2
			self.centerY = self.height//2


		def reset(self):
			"""
			sets the mouse position to the center of the screen.
			"""
			self.bge.logic.mouse.position = (0.5, 0.5)


		def show(self, vis=1):
			"""
			makes the mouse visible.
			"""
			self.bge.logic.mouse.visible = vis

		def hide(self, vis=0):
			"""
			hides the mouse from view.
			"""
			self.bge.logic.mouse.visible = vis

		def getPosition(self):
			"""
			returns the position of the mouse. X, Y
			"""
			position = self.bge.logic.mouse.position

			X = position[0]*self.width
			Y = position[1]*self.height

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
			if self.bge.logic.mouse.events[self.bge.events.MOUSEX] or self.bge.logic.mouse.events[self.bge.events.MOUSEY]:
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
		
		mouse = None
		
		other = []

		

		def __init__(self):
			import bge

			#finding sensors
			KEYBOARD = bge.logic.keyboard
			
			MOUSE = bge.logic.mouse
			
			###

			#setting variables.=
			self.keyboard = KEYBOARD
			
			self.mouse = MOUSE
			
			self.other.append("LMB")
			self.other.append("RMB")
			self.other.append("MMB")

			self.other.append("MWU")
			self.other.append("MWD")



			

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
				
			def convertMouseControl(self, control):
				"""
				converts a special mouse options value to a bge.events value.
				"""
				newControl = ""
				
				if control[1:] == "MB":
					if control[0] == "L":
						newControl += "LEFT"
					elif control[0] == "R":
						newControl += "RIGHT"
					else:
						newControl += "MIDDLE"
				else:
					if control == "MWU":
						newControl += "WHEELUP"
					else:
						newControl += "WHEELDOWN"
					
				newControl += "MOUSE"
				return newControl

			def getValue(self, value=None):
				"""
				converts the options value to a bge.events value.
				"""
				if not value:
					if control not in self.controller.controls:
						return None
					value = self.controller.controls[self.control]
					
				value = value.replace("-", "")
				value = value.upper()
				
				if value in self.controller.other:
					value = self.convertMouseControl(value)
					
				self.value = value
					
				return value

			

			def getStatus(self):
				"""
				figures out the status of the event. (0 for inactive, 1 for just pressed, 2 for held, 3 for just released.)
				"""
				import bge
				if "MOUSE" in self.value:
					self.kind = "other"

					status = self.controller.mouse.events[getattr(bge.events, self.value)]
					return status
				
				else:
					self.kind = "key"
					status = self.controller.keyboard.events[getattr(bge.events, self.value)]
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

			for control in self.controls:
				value = self.controls[control]
				event = self.EVENT(self, control, value)
				self.events[control] = event

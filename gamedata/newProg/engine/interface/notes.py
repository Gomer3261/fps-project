##############################################
### ====================================== ###
### ======		 Note System!		====== ###
### ====================================== ###
##############################################
import engine.interface.bgui as bgui

class initializeNotificationSystem:
	"""
	The Notification class manages all notifications and alerts.
	This involves making sure all notes and alerts are displayed to the user,
	Notes and alerts are not displayed the second they are requested.
	"""
	
	def __init__(self, interface, bgui):
		"""
		Initializing the notification system.
		And yes, I use objects because I don't want global variables.
		Deal with it.
		"""
		self.interface = interface
		self.bgui = bgui
		
		self.notes = []
		self.alerts = []
		self.activeNote = None
		self.activeAlert = None
		
	def requestNote(self, text="Error", time=None):
		"""
		Leaves a request for a note to the player in the noficiation system.
		"""
		self.notes.append((text, time))
		
	def requestAlert(self, text="Error", buttons=None):
		"""
		Leaves a request for an alert to the player in the notification system.
		requests are in the form, text, buttons where buttons is a list of tuples consising of text and callback objects.
		e.g. [("exit", bge.endGame), ("continue", None)]
		A button with no callback will close the window.
		An empty button list will allow the user to close the window by pressing anywhere on the alert.
		"""
		self.alerts.append((text, buttons))
		
	def main(self):
		"""
		The main function ensures that either a note and alert are displaying or notes and alerts are empty.
		The function also runs each note and alert to ensure they are in the correct state for rendering.
		"""
		if self.activeAlert:
			self.activeAlert.main()
		elif self.alerts:
			self.activeAlert = self.initializeAlert(self, self.bgui, self.alerts[0])
			self.activeAlert.main()
			del self.alerts[0]
		
		if self.activeNote:
			self.activeNote.main()
		elif self.notes:
			self.activeNote = self.initializeNote(self, self.bgui, self.notes[0])
			self.activeNote.main()
			del self.notes[0]
	
	def renderNote(self):
		"""
		Renders the current note.
		"""
		if self.activeNote:
			self.activeNote.render()
	
	#These functions are split to allow the interface to order them however it wants.
	def renderAlert(self):
		"""
		Renders the current alert
		"""
		if self.activeAlert:
			self.activeAlert.render()
			
			
			
			
			
			
			
			
			
			

	class initializeNote(bgui.System):
		"""
		A notification is a small message that appears in the top right of the players screen.
		It lasts for a short period of time before deleting itself.
		The note class is responsible for displaying itself and handling it's own animations.
		"""
		showTime = 0.20
		hideTime = 0.20
		
		def __init__(self, notificationSystem, bgui, args):
			"""
			Creates the note object.
			initializes bgui objects.
			calculates display time.
			"""
			import time
			self.time = time
			
			self.notificationSystem = notificationSystem
			self.bgui = bgui
			self.text = args[0]

			if not args[1]:
				self.displayTime = (float(len(self.text)) * 0.05) + 1.0 # Dynamic Display Time (0.05 seconds per character)
			else:
				self.displayTime = args[1]
				
			self.startTime = self.time.time()
			
			#Bgui object initialization
			bgui.System.__init__(self)
			
			self.frame = bgui.Frame(self, 'note', border=1, size=[0.3, 0.2], pos=[0.7, 0.8])
			self.frame.colors = [(0.2, 0.2, 0.2, 0.0) for i in range(4)]
			
			self.display = bgui.TextBlock(self.frame, 'note_text', text=self.text, color=(1, 1, 1, 1), pt_size=40, size=[0.95, 0.90],
				options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX | bgui.BGUI_CENTERY, overflow=bgui.BGUI_OVERFLOW_HIDDEN)
			
		def main(self):
			"""
			Animates and kills the note.
			"""
			factor = 0.0
			if self.time.time() > (self.startTime + self.showTime + self.displayTime + self.hideTime):
				self.end()
			elif self.time.time() > (self.startTime + self.showTime + self.displayTime):
				#Hide animation will occur here.
				factor = (self.hideTime - (self.time.time() - (self.startTime + self.showTime + self.displayTime))) / self.hideTime
				self.frame.colors = [(0.2, 0.2, 0.2, (0.8 * factor)) for i in range(4)]
				self.frame._update_position(self.frame._base_size, [0.7, (1.0 - (0.2 * factor))])
				self.display._update_position(self.display._base_size, self.display._base_pos)
				self.display.text = self.text
			
			elif self.time.time() > (self.startTime + self.showTime):
				if self.frame._base_pos != [0.7, 0.8]:
					self.frame._update_position(self.frame._base_size, [0.7, 0.8])
					self.display._update_position(self.display._base_size, self.display._base_pos)
					self.display.text = self.text
			
			else:
				#play show animation.
				factor = (self.time.time() - self.startTime) / self.showTime
				self.frame.colors = [(0.2, 0.2, 0.2, (0.8 * factor)) for i in range(4)]
				self.frame._update_position(self.frame._base_size, [0.7, (1.0 - (0.2 * factor))])
				self.display._update_position(self.display._base_size, self.display._base_pos)
				self.display.text = self.text
				
				
		def end(self):
			"""
			Ends the notification so a new one can be displayed.
			"""
			#kill bgui objects
			self.notificationSystem.activeNote = None
			self._remove_widget(self.frame)
			
			
			
			
			
			
			
			
	class initializeAlert(bgui.System):
		"""
		Alerts are a popup window that forces the user to acknowledge it.
		Alerts are able to accept callback buttons, but will default to closing themselves if none are provided.
		Alerts appear above all other UIs and lock everything that uses the mouse.
		"""
		def __init__(self, notificationSystem, bgui, args):
			
			self.notificationSystem = notificationSystem
			self.bgui = bgui
			self.text = args[0]
			self.buttons = []
			
			buttonData = args[1]
			
			import bge
			bge.logic.mouse.visible = True
			
			import engine
			engine.interface.mouse.reserved += 1
			
			#Bgui object initialization
			bgui.System.__init__(self)
			
			self.background = bgui.Frame(self, 'alert_background', border=0, size=[1.0, 1.0], pos=[0.0, 0.0])
			self.background.colors = [(0.0, 0.0, 0.0, 0.8) for i in range(4)]
			
			self.frame = bgui.Frame(self.background, 'alert', border=1, size=[0.4, 0.4], options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CENTERY)
			self.frame.colors = [(0.2, 0.2, 0.2, 0.8) for i in range(4)]
			
			self.display = bgui.TextBlock(self.frame, 'note_text', text=self.text, color=(1, 1, 1, 1), pt_size=40, size=[0.95, 0.90],
				options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX | bgui.BGUI_CENTERY, overflow=bgui.BGUI_OVERFLOW_HIDDEN)
				
			if not buttonData:
				self.display.on_click = self.end
			else:
				for i in range(len(buttonData)):
					self.buttons.append(bgui.FrameButton(self.frame, ('alert_button_' + str(i)), text=buttonData[i][0], size=[(0.9/len(buttonData)), 0.1], pos=[0.05+(0.9/len(buttonData)*i), 0.05],
						options = bgui.BGUI_DEFAULT))
					if buttonData[i][1]:
						self.buttons[i].on_click = buttonData[i][1]
					else:
						self.buttons[i].on_click = self.end
			
		def main(self):
			"""
			Updates the current mouse information for bgui.
			"""
			# Handle the mouse
			import bge
			mouse = bge.logic.mouse
			
			pos = list(mouse.position)
			pos[0] *= bge.render.getWindowWidth()
			pos[1] = bge.render.getWindowHeight() - (bge.render.getWindowHeight() * pos[1])
			
			mouse_state = bgui.BGUI_MOUSE_NONE
			mouse_events = mouse.events
					
			if mouse_events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_JUST_ACTIVATED:
				mouse_state = bgui.BGUI_MOUSE_CLICK
			elif mouse_events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_JUST_RELEASED:
				mouse_state = bgui.BGUI_MOUSE_RELEASE
			elif mouse_events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_ACTIVE:
				mouse_state = bgui.BGUI_MOUSE_ACTIVE
			
			self.update_mouse(pos, mouse_state)
				
		def end(self, arg2=None):
			"""
			Ends the notification so a new one can be displayed.
			"""
			import bge
			bge.logic.mouse.visible = False
			
			import engine
			engine.interface.mouse.reserved -= 1
			
			#kill bgui objects
			self.notificationSystem.activeAlert = None
			self._remove_widget(self.background)
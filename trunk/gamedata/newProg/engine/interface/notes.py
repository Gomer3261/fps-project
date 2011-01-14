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
		if self.activeAlert:
			self.activeAlert.main()
		elif self.alerts:
			#self.activeAlert = self.initializeAlert(self, self.bgui, self.alerts[0])
			self.activeAlert.main()
			del self.alerts[0]
		
		if self.activeNote:
			self.activeNote.main()
		elif self.notes:
			self.activeNote = self.initializeNote(self, self.bgui, self.notes[0])
			self.activeNote.main()
			del self.notes[0]
	
	def render(self):
		if self.activeNote:
			self.activeNote.render()
		if self.activeAlert:
			self.activeAlert.render()

	class initializeNote(bgui.System):
		"""
		A notification is a small message that appears in the top right of the players screen.
		It lasts for a short period of time before deleting itself.
		The note class is responsible for displaying itself and handling it's own animations.
		"""
		noteShowTime = 0.25
		noteHideTime = 0.25
		
		def __init__(self, notificationSystem, bgui, args):
			import time
			self.time = time
			
			self.notificationSystem = notificationSystem
			self.bgui = bgui
			self.text = args[0]

			if not args[1]:
				self.displayTime = (float(len(self.text)) * 0.08) + 0.5 # Dynamic Display Time (0.05 seconds per character)
			else:
				self.displayTime = args[1]
				
			self.startTime = self.time.time()
			
			#Bgui object initialization
			bgui.System.__init__(self)
			
			self.frame = bgui.Frame(self, 'note', border=1, size=[0.3, 0.2], pos=[0.7, 0.8])
			self.frame.colors = [(0.2, 0.2, 0.2, 0.8) for i in range(4)]
			
			self.display = bgui.TextBlock(self.frame, 'note_text', text=self.text, color=(1, 1, 1, 1), pt_size=40, size=[0.95, 0.90],
				options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX | bgui.BGUI_CENTERY, overflow=bgui.BGUI_OVERFLOW_HIDDEN)
			
		def main(self):
			if self.time.time() > (self.startTime + self.noteShowTime + self.displayTime + self.noteHideTime):
				self.end()
			elif self.time.time() > (self.startTime + self.noteShowTime + self.displayTime):
				#play end animation
				pass
			elif self.time.time() > self.startTime:
				#play show animation.
				pass
				
		def end(self):
			#kill bgui objects
			self.notificationSystem.activeNote = None
			self._remove_widget(self.frame)

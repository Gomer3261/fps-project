##############################################
### ====================================== ###
### ======		 Note System!		====== ###
### ====================================== ###
##############################################

class Class:
	"""
	The Notification class manages all notifications.
	This involves making sure all notifications are displayed to the user,
	and insuring animations are given time to complete.
	
	Please note that notifications are not displayed the second they are requested.
	"""
	# The times it takes for the notifier to play
	# it's hiding and showing animations...
	noteShowTime = 0.25
	noteHideTime = 0.25

	def __init__(self):
		# Adding the Notes scene.
		import GameLogic as gl
		con = gl.getCurrentController()
		
		openNotes = con.actuators["ADDOVERLAY"]
		openNotes.scene = "Notes"
		con.activate(openNotes)
		
		# A note looks like (text, time)
		self.notes = []

		# When active, we are currently in the process of "notifying" the user.
		self.active = 0

		# This shows/hides the notification panel.
		self.show = 0

		# The current note text to display
		self.currentText = ""

		self.displayTime = 0.0
		self.startTime = 0.0
		self.currentTime = 0.0
		
		print("  Interface/Notes are good to go.")







	def notify(self, text, time=0.0):
		"""
		Adds a notification to the display que.
		"""
		self.notes.append((text, time))

	def run(self):
		"""
		Runs the notification object on the notes scene.
		"""
		import time
		import GameLogic as gl
		con = gl.getCurrentController()
		
		# If the notifier is not active, and is ready for the next note...
		if not self.active:
			# And there is a note read in the queue...
			if self.notes:
				# Get the next note
				note = self.notes.pop(0) # note looks like (text, time)
				
				# Textwrapping
				import textwrap
				self.currentText = textwrap.fill(note[0], 32)
				
				# Set the display time
				if not note[1]:
					#FAST-READER# self.displayTime = (float(len(note[0])) * 0.05) + 0.5 # Dynamic Display Time (0.05 seconds per character)
					self.displayTime = (float(len(note[0])) * 0.08) + 0.5 # Dynamic Display Time (0.05 seconds per character)
				else:
					self.displayTime = note[1]
				
				self.displayTime += self.noteShowTime
				
				self.active = 1 # It's now active (not ready to take another note yet)
				self.show = 1 # This is the signal for the notifier to pop out and display it's note text
				self.startTime = time.time() # Starting the timer...
		else:
			# Okay, so we're getting the time that the note has been active
			self.currentTime = time.time() - self.startTime
			
			# When the note has been active for the display time, then it's time to stop showing.
			if self.currentTime > self.displayTime:
				self.show = 0
			
			# Just because we're done showing doesn't mean we're ready for the next note; the notifier
			# neets some time to play it's hiding animation, only once that is done may we do the next note
			if self.currentTime > (self.displayTime + self.noteHideTime):
				self.active = 0
		
		
		
		# Okay, so we've got all our information for our notifier object,
		# so now we just give it to the object so it can display it graphically :)
		obj = con.owner
		textObj = con.actuators["noteText"].owner
		textObj["Text"] = self.currentText
		obj["show"] = self.show

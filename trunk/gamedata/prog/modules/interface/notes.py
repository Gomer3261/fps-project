##############################################
### ====================================== ###
### ======		 Note System!		====== ###
### ====================================== ###
##############################################

INIT = 1

# The times it takes for the notifier to play
# it's hiding and showing animations...
noteShowTime = 0.25
noteHideTime = 0.25






# A note looks like (text, time)
notes = []

# When active, we are currently in the process of "notifying" the user.
active = 0

# This shows/hides the notification panel.
show = 0

# The current note text to display
currentText = ""

displayTime = 0.0
startTime = 0.0
currentTime = 0.0







def notify(text, time=0.0):
	global notes
	notes.append((text, time))

def run(con):
	global notes, active, show, currentText
	global noteShowTime, noteHideTime
	import time
	
	# If the notifier is not active, and is ready for the next note...
	if not active:
		# And there is a note read in the queue...
		if notes:
			# Get the next note
			note = self.notes.pop(0) # note looks like (text, time)
			
			# Textwrapping
			import textwrap
			currentText = textwrap.fill(text, 34)
			
			# Set the display time
			if not note[1]:
				displayTime = (float(len(note[0])) * 0.05) + 0.5 # Dynamic Display Time (0.05 seconds per character)
			else:
				displayTime = note[1]
			
			displayTime += noteShowTime
			
			active = 1 # It's now active (not ready to take another note yet)
			show = 1 # This is the signal for the notifier to pop out and display it's note text
			startTime = time.time() # Starting the timer...
	else:
		# Okay, so we're getting the time that the note has been active
		currentTime = time.time() - startTime
		
		# When the note has been active for the display time, then it's time to stop showing.
		if currentTime > displayTime:
			show = 0
		
		# Just because we're done showing doesn't mean we're ready for the next note; the notifier
		# neets some time to play it's hiding animation, only once that is done may we do the next note
		if currentTime > (displayTime + noteHideTime):
			active = 0
	
	
	
	# Okay, so we've got all our information for our notifier object,
	# so now we just give it to the object so it can display it graphically :)
	obj = con.owner
	obj["Text"] = currentText
	obj["show"] = show

# gncore: for communication with gameplay servers





gnclient = None

import handlers
class GNCLIENT(handlers.CLIENT):
	
	ticket = None # You cannot send any data over UDP until you get your ticket.
	
	def requestTicket(self):
		self.send("ticket", "plz")

	def joinGame(self, name):
		self.send("join", name)

expiration = 5.0
gnclient = GNCLIENT(expiration)





class TIMER():
	import time
	last = 0.0
	def __init__(self):
		self.reset()

	def reset(self):
		self.last = self.time.time()

	def get(self):
		dif = self.time.time() - self.last
		return dif
	
	def do(self, interval=1.0):
		# This is useful for an interval timer.
		# If you want something to happen every
		# interval seconds, call this function
		# and if it returns 1, then do it.
		# In other words, this returns 1 after
		# the given interval time has elapsed since
		# 1 was last returned. Get it?
		dif = self.get()
		if dif > interval:
			self.reset()
			return 1 # Do
		else:
			return 0 # Don't.



# Use this for determining if it's time for a basic update.
# (sending the player's basic information to the server).
basicUpdateTimer = TIMER()

# Sent to the server to keep the server aware
# that the client is happily connected.
checkTimer = TIMER()

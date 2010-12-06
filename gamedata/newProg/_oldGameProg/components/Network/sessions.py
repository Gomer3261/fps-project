class SESSIONSTORAGE:
	"""
	A Network thing.
	Stores sessions, which allows a dropped player to quickly rejoin 
	the game without having to totally reconnect and crap, easily 
	maintaining the same UID and stuff.
	"""
	
	################################################
	class SESSION:
		def __init__(self, clientSock=None, sessionTimeout=60.0):
			self.clientSock = clientSock
			self.udp = None
			self.UID = None
			self.sessionTimeout = sessionTimeout
			import comms
			self.sessionTimeoutClock = comms.TIMER()
		def hasGoneStale(self):
			if not self.clientSock and (self.sessionTimeoutClock.get() > self.sessionTimeout):
				return True
			else:
				return False
		def terminateClientSock(self):
			if self.clientSock:
				self.clientSock.terminate()
				self.clientSock = None
				self.udp = None
				self.sessionTimeoutClock.reset()
	################################################
	
	def __init__(self):
		self.sessions = {}
		self.nextTicket = 1
	
	def grabTicket(self):
		ticket = self.nextTicket
		self.nextTicket += 1
		return ticket
	
	def newSession(self, clientSock=None):
		ticket = self.grabTicket()
		session = self.SESSION(clientSock)
		self.sessions[ticket] = session
		return ticket, session
	
	def deleteSession(self, ticket):
		del self.sessions[ticket]
	
	def getSession(self, ticket):
		return self.sessions[ticket]

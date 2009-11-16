### MasterServerNetworking Module ###

class Class:
	"""
	This object handles all communications with the Master Server.
	A dictionary, ms_session, can be saved and later reused to recover a session.
	All information about our current session is stored in ms_session.
	"""

	def __init__(self):
	
		self.ms_session = {}
		
		self.ms_session["sock"] = None # the socket object.
		self.ms_session["connection"] = 0 # 0: no connection. 1: connected. -1: currently attempting connection.
		self.ms_session["host"] = ""
		self.ms_session["port"] = 0
		
		self.ms_session["ticket"] = 0
		self.ms_session["loggedIn"] = 0
		self.ms_session["userName"] = ""
		self.ms_session["userPassword"] = ""
		
		self.ms_session["inBuffer"] = ""
		self.ms_session["outBuffer"] = ""
		self.ms_session["lastTime"] = 0.0
	
	
	
	
	
	### ================================================
	### Run Method
	### ================================================
	
	def run(self):
		
		# Asynchronous Connection
		if self.ms_session["connection"] == -1:
			self.checkConnectionStatus()
		
		# Receiving data to the inBuffer
		self.recv()
		# Handling data in the inBuffer
		self.handleIn()
		
		# Sending data that is in the outBuffer.
		self.handleOut()
	
	
	
	
	### ================================================
	### Basic Socket Operations
	### ================================================

	def makeSocket(self):
		"""
		Just makes a new non-blocking socket.
		"""
		import socket
		self.ms_session["sock"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ms_session["sock"].setblocking(0)

	def startConnection(self):
		"""
		Starts a connection to the Master Server based on the session's information.
		"""
		self.ms_session["connection"] = -1
		pass

	def checkConnectionStatus(self):
		"""
		Checks if we are connected. If we are, connection info is set to 1.
		Necessary for asynchronous connection.
		"""
		pass
	
	
	
	### ================================================
	### Special Socket Operations
	### ================================================
	
	def reconnect(self, new_ms_session):
		"""
		Reconnects to the new_ms_session based on the information within it.
		"""
		self.ms_session = new_ms_session
		self.startConnection()
		self.reclaimSession()
	
	def reclaimSession(self)
		"""
		Sends a message to the server to tell it that we are reclaiming our session.
		It should remember who we are.
		"""
		self.send( "message to claim session with ticket: %s"%(self.ms_session["ticket"]) )
	
	
	
	### ================================================
	### In/Out Handling
	### ================================================
	
	def recv(self, buf):
		"""
		Receiving data from the socket, adding it to the inBuffer.
		"""
		pass
	
	def handleIn(self):
		"""
		Handles data that's in the inBuffer.
		"""
		pass
	
	def send(self, data):
		"""
		Adds data to the outBuffer.
		"""
		pass
	
	def handleOut(self):
		"""
		Sends the data in the outBuffer through the socket, retaining the leftovers to try
		again next run.
		"""
		pass

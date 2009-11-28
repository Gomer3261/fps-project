### GameplayServer Networking Module ###

class Class:
	"""
	GameplayServer Networking.
	
	Master Public Interface:
		- run(MasterInfo): Performs special high-level operations like connecting, reconnecting, etc.
		- incoming(): Receives data from a remote host.
		- outgoing(LocalGame): Sends data from the out buffers (sendBuffer and throwBuffer) to 
			the host. When you are playing offline, you are the host, and in this case the data
			is just fed back to the in buffers (no real networking required).
	
	Lower-level Public Interface:
		- send(package): sends a package (by placing it in the sendBuffer, where it is later handled by the outgoing loop).
		- throw(package): sends a package over UDP (by placing it in the throwBuffer, where it is later handled by the outgoing loop).
		- getinItems(): gets a list of items we have received this tick. These items will be cleared next tick.
	
	"""

	def __init__(self):
	
		self.gps_session = {}
		
		self.gps_session["sock"] = None # When connected, this is a pair (UDP, TCP).
		self.gps_session["connection"] = (0, 0) # (UDP_conn, TCP_conn) 0: no connection. 1: connected. -1: currently attempting connection.
		self.gps_session["address"] = "192.168.1.1:3201/3202" # Standard address protocol for a gps_session
		
		self.gps_session["ticket"] = -1
		self.gps_session["inBuffer"] = ""
		self.gps_session["outBuffer"] = ""
		self.gps_session["lastTime"] = 0.0
		
		self.inItems = []
		self.sendBuffer = []
		self.throwBuffer = []
	
	
	
	### ================================================
	### Run Method
	### ================================================
	
	def run(self, MasterInfo):
		"""
		Performs special high-level operations like connecting, reconnecting, etc.
		"""
		pass
	
	
	
	
	
	### ================================================
	### IO Interface
	### ================================================
	
	def send(self, package):
		"""
		Puts a package into the sendBuffer
		"""
		self.sendBuffer.append(package)
	
	def throw(self, package):
		"""
		Puts a package into the throwBuffer
		"""
		self.throwBuffer.append(package)
	
	def getInItems(self):
		return self.inItems
	
	
	
	
	
	### ================================================
	### Incoming
	### ================================================
	
	def incoming(self):
		"""
		Receiving data to the inBuffer, then extracting it from the inBuffer to the inItems list.
		inItems is cleared before the new items are put in there.
		"""
		self.recv()
		#self.inItems = []
		self.extract()
	
	def recv(self, buf=2048):
		"""
		Receives data from the TCP socket, adds it to the inBuffer
		Then, it receives UDP items and immediately plops it into inItems.
		"""
		pass
		# Doing TCP
		#data = ""
		#self.gps_session["inBuffer"] += data
		
		# Doing UDP
		#data = ""
		#item = [None, None] # unflattenUDP(data)
		#self.inItems.append(item)
	
	def extract(self):
		"""
		Extracts flattened packages from the inBuffer, puts them in the inItems list.
		"""
		pass
		#items = self.gps_session["inBuffer"]
		#for item in items:
		#	self.inItems.append(item)
	
	
	
	
	
	### ================================================
	### Outgoing
	### ================================================
	
	def outgoing(self, Admin):
		"""
		sends stuff in the outgoing buffers.
		"""
		self.sendAndThrowBuffers(Admin)
		self.handleOutBuffer()
	
	def sendAndThrowBuffers(self, Admin):
		"""
		Sends out data that has accumulated in the buffers.
		Requires LocalGame to get the Director entity (not anymore).
		If we own the GameState, then outgoing data will just
		be plopped right into inItems.
		"""
		#director = LocalGame.getDirector()
		
		ourUID = 1
		
		# We own the GameState
		if True: #Admin.weOwnGameState():
			# Feedback loop; placing packages straight into our own inItems list.
			for package in self.sendBuffer:
				self.inItems.append([ourUID, package])
			for package in self.throwBuffer:
				self.inItems.append([ourUID, package])
		else:
			# Hehe, like this will ever happen...
			# Flattening the packages and sending them off to a remote host.
			for package in self.sendBuffer:
				data = [None, None] # flatten(package)
				self.gps_session["outBuffer"] += data
			for package in self.throwBuffer:
				data = [None, None] # flatten(package)
				# now we're supposed to send it over UDP.
		
		self.sendBuffer = []
		self.throwBuffer = []
	
	
	def handleOutBuffer(self):
		"""
		Sends the data in the outBuffer through the socket, retaining the leftovers to try
		again next run.
		"""
		return None
		data = self.gps_session["outBuffer"] # Sends this through the socket.

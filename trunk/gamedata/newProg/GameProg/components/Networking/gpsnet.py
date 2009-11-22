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
		- getInPackages(): gets a list of packages we have received this tick. These packages will be cleared next tick.
	
	"""

	def __init__(self):
	
		self.gps_session = {}
		
		self.gps_session["sock"] = None # When connected, this is a pair (UDP, TCP).
		self.gps_session["connection"] = (0, 0) # (UDP_conn, TCP_conn) 0: no connection. 1: connected. -1: currently attempting connection.
		self.gps_session["address"] = "192.168.1.1:3201/3202" # Standard address protocol for a gps_session
		
		self.gps_session["ticket"] = 0
		self.gps_session["inBuffer"] = ""
		self.gps_session["outBuffer"] = ""
		self.gps_session["lastTime"] = 0.0
		
		self.inPackages = []
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
	
	def getInPackages(self):
		return self.inPackages
	
	
	
	
	
	### ================================================
	### Incoming
	### ================================================
	
	def incoming(self):
		"""
		Receiving data to the inBuffer, then extracting it from the inBuffer to the inPackages list.
		inPackages is cleared before the new packages are put in there.
		"""
		self.recv()
		self.inPackages = []
		self.extract()
	
	def recv(self, buf=2048):
		"""
		Receives data from the TCP socket, adds it to the inBuffer
		Then, it receives UDP packages and immediately plops it into inPackages.
		"""
		# Doing TCP
		data = ""
		self.gps_session["inBuffer"] += data
		
		# Doing UDP
		data = ""
		package = [None, None] # unflattenUDP(data)
		self.inPackages.append(package)
	
	def extract(self):
		"""
		Extracts flattened packages from the inBuffer, puts them in the inPackages list.
		"""
		packages = self.gps_session["inBuffer"]
		for package in packages:
			self.inPackages.append(package)
	
	
	
	
	
	### ================================================
	### Outgoing
	### ================================================
	
	def outgoing(self, LocalGame):
		"""
		"""
		self.sendAndThrowBuffers(LocalGame)
		self.handleOutBuffer()
	
	def sendAndThrowBuffers(self, LocalGame):
		"""
		Sends out data that has accumulated in the buffers.
		Requires LocalGame to get the Director entity.
		If we own the GameState, then outgoing data will just
		be plopped right into inPackages.
		"""
		director = LocalGame.getDirector()
		
		if director.weOwnGameState():
			# Feedback loop; placing packages straight into our own inPackages list.
			for package in self.sendBuffer:
				self.inPackages.append(package)
			for package in self.throwBuffer:
				self.inPackages.append(package)
		else:
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

### GameplayServer Networking Module ###

class Class:
	"""
	GameplayServer Networking.
	
	The gpsnet is used by any part of the game, usually entities, to access and manipulate the GameState
	of the host, be it local, or remote over the internet.
	
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

	def __init__(self, slab):
		self.slab = slab
	
		self.gps_session = {}
		
		self.gps_session["server"] = None # Server Object
		self.gps_session["client"] = None # Client Object
		self.gps_session["connection"] = (0, 0) # (UDP_conn, TCP_conn) 0: no connection. 1: connected. -1: currently attempting connection.
		self.gps_session["address"] = "chasemoskal.dyndns.org:3201/3202" # Standard address protocol for a gps_session
		
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
	
	def run(self, Admin, Interface):
		"""
		Performs special high-level operations like connecting, reconnecting, etc.
		"""
		self.runServer(Admin, Interface)
		self.runClient(Admin, Interface)
	
	def runServer(self, Admin, Interface):
		server = self.gps_session['server']
		if server:
			bundles, newConnections, staleClients, staleSessions = server.run()
			for bundle in bundles:
				ticket, item = bundle
				flag, data = item
				if flag == 'MSG':
					Interface.terminalOutputWithNotification("SVR: MSG(%s): %s"%(ticket, data))
			for newConnection in newConnections: Interface.Terminal.output("SVR: (%s) Connected (ticket=%s)."%newConnection)
			for staleClient in staleClients: Interface.Terminal.output("SVR: Client (%s) from session %s went stale."%staleClient)
			for staleSession in staleSessions: Interface.Terminal.output("SVR: Session %s went stale."%staleSession)
	
	def runClient(self, Admin, Interface):
		client = self.gps_session['client']
		if client:
			items, hasGoneStale, justConnected = client.run()
			if justConnected:
				import comms; addressString = comms.makeAddressString(client.address)
				Interface.terminalOutputWithNotification("CL: Connected to (%s)!"%addressString)
			for item in items:
				flag, data = item
				if flag == "MSG":
					sender, message = data
					Interface.terminalOutputWithNotification("(%s): %s"%(sender, message))
			if hasGoneStale:
				import comms; addressString = comms.makeAddressString(client.address)
				Interface.terminalOutputWithNotification("CL: Connection to (%s) failed/went stale."%(addressString))
				client.terminate()
				self.gps_session['client'] = None
	
	def startClient(self, address="chasemoskal.dyndns.org:3205"):
		import classes
		import comms
		addressTuple = comms.makeAddressTuple(address)
		print("Starting connection to", addressTuple)
		self.gps_session['client'] = classes.TCP_CLIENT(addressTuple)
		self.gps_session['client'].initiateConnection()
	
	def startServer(self, address=":3205"):
		import classes
		import comms
		addressTuple = comms.makeAddressTuple(address)
		self.gps_session['server'] = classes.TCP_SERVER(addressTuple)
		#print(self.gps_session['server'])
		bound = self.gps_session['server'].bind()
		#print(self.gps_session['server'])
		if bound:
			self.slab.Interface.Terminal.output("Server is bound and running...")
		else: 
			self.slab.Interface.Terminal.output("Error: Server failed to bind.")
			self.gps_session['server'] = None
		#print(self.gps_session['server'])
	
	def endServer(self):
		self.gps_session['server'].terminate()
		self.gps_session['server'] = None
		self.slab.Interface.Terminal.output("Server terminated.")
	
	
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
		
		ourUID = Admin.getUID()
		
		# We own the GameState
		if True: #Admin.weOwnGameState():
			# Feedback loop; placing packages straight into our own inItems list.
			for package in self.sendBuffer:
				self.inItems.append( (ourUID, package) )
			for package in self.throwBuffer:
				self.inItems.append( (ourUID, package) )
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

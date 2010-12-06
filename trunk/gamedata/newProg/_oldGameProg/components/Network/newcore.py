# The New Core #

class GAMEPLAYSERVER:
	def __init__(self):
		"""
		An initiation of all the variables we'll be using.
		"""
		import comms; self.comms = comms
		self.active = False
		#
		self.addressString = ""
		self.addressTuple = (None, None)
		#
		self.tcpServer = None
		self.udpServer = None
		#
		self.greeted = False
		#
		self.tcpBytesIn = 0
		self.tcpBytesOut = 0
		#
		self.udpBytesIn = 0
		self.udpBytesOut = 0
		#
		self.nextTicket = 1
		self.sessions = {} # A dictionary of sessions stored by Network ticket
	
	def establish(self, addressString):
		self.addressString=addressString; self.addressTuple=self.comms.makeAddressTuple(addressString)
		IP, port = self.addressTuple
		#
		import socket
		#
		self.tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.tcpServer.settimeout(0.0); self.tcpServer.setblocking(0); self.tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.tcpServer.bind( ("", port) )
		#
		self.udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.udpServer.settimeout(0.0); self.udpServer.setblocking(0); self.udpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.udpServer.bind( ("", port) )
		
		self.greeted = False
		self.active = True
	
	########################################################################################################################
	class SESSION:
		def __init__(self, gameplayserver):
			import comms; self.comms = comms
			self.active = False
			self.gameplayserver = gameplayserver
			# Associations
			self.tcpSock = None
			self.tcpAddr = None
			self.udpServer = None
			self.udpAddr = None # The UDP address of the client.
			self.UID = None
			# Streams and Buffers
			self.tcpInstream = comms.STREAM()
			self.tcpOutbuffer = ""
			# Results
			self.tcpInItems = []
			self.udpInItems = []
			#
			self.timeoutClock = comms.TIMER()
			self.timeout = 6.0
			
		def initialAssociation(self, tcpSock, tcpAddr, udpServer):
			self.tcpSock = tcpSock
			self.tcpAddr = tcpAddr
			self.udpServer = udpServer
		
		def associateUdpAddr(self, udpAddr):
			self.udpAddr = udpAddr
		
		def run(self):
			"""
			Executes IO (Input/Output)
			? - Extracts packages out of the instreams.
			Handles staleness.
			"""
			self.IO()
			if self.hasGoneStale(): self.active = False
		
		def IO(self):
			"""
			TCP:
				Adds data to the tcpInstream (by receiving it)
				Clears data out of the tcpOutbuffer (by sending it).
			"""
			# TCP RECV
			try:
				data = self.tcpSock.recv(4096):
				if data:
					self.gameplayserver.tcpBytesIn += len(data)
					self.tcpInstream.add(data)
					self.timeoutClock.reset()
			except: pass
			# TCP SEND
			try:
				if self.tcpOutbuffer:
					sent = self.tcpSock.send(self.tcpOutbuffer)
					self.tcpOutbuffer = self.tcpOutbuffer[sent:]
					self.gameplayserver.tcpBytesOut += sent
			except: pass
		
		def send(self, item):
			package = self.comms.pack(item)
			self.tcpOutbuffer += package
		
		def recv(self):
			items = self.tcpInItems
			self.tcpInItems = []
			return items
		
		def throw(self, item):
			try:
				if self.udpAddr:
					package = self.comms.pack(item)
					self.udpServer.sendto(package, self.udpAddr)
					self.gameplayserver.udpBytesOut += len(package)
			except: pass
		
		def catch(self):
			# We don't actually recieve from the UDP socket from here, because of the way UDP works.
			# but we pretend that we do, just for the sake of... consistency?
			items = self.udpInItems
			self.udpInItems = []
			return items
		
		def hasGoneStale(self):
			if self.timeoutClock.get() > self.timeout: return True
			else: return False
		
	########################################################################################################################
	
	def run(self):
		self.acceptTcpConnections()
		self.udpIn()
		self.runEachSession()
	
	def acceptTcpConnections(self):
		"""
		Accepts a TCP connection and creates a new session for it; it associates the new TCP socket with the session.
		"""
		try:
			self.tcpServer.listen(3)
			sock, addr = self.tcpServer.accept()
			
			if sock:
				session = self.SESSION(self)
				session.initialAssociation(sock, addr, self.udpServer)
				ticket = self.nextTicket; self.nextTicket += 1
				self.sessions[ticket] = session
		except:
			pass
	
	def udpIn(self, attempts=10):
		"""
		Handles incoming data from the UDP Server.
		We break incoming packets down into the network ticket it belongs to, and the package.
		If it doesn't come with a network ticket referring to a valid session, the whole packet is ignored.
		If the ticket does refer to a network ticket, then we associate the UDP information with the session,
		and the package is added to that session's udpInpackages list. This session association system is necessary to
		keep track of which data is who's -- it allows send, recv, throw, and catch methods all to be located
		on each session, which simplifies things for everybody.
		"""
		for i in range(attempts):
			try:
				package, addr = udpServer.recvfrom(4096)
				if package:
					self.udpBytesIn += len(package)
					ticket, item = self.comms.unpackUDP(package)
					session = self.getSession(ticket)
					if session:
						if not session.udpAddr: session.associateUdpAddr(addr)
						session.udpInItems.append(item)
			except: break
		#####
	
	def runEachSession(self):
		"""
		Runs each session so that it works.
		"""
		for ticket in self.sessions: self.sessions[ticket].run()
	
	def getSession(self, ticket):
		# is this function kinda stupid?
		if ticket in self.sessions:
			session = self.sessions[ticket]
			return session
		else:
			return None

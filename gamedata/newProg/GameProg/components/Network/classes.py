### Low-level Networking Classes ###


###### ### ################################ ### ######
###### ### ### ------ TCP SERVER ------ ### ### ######
###### ### ################################ ### ######

class TCP_SERVER:
	def __init__(self, address):
		self.address = address
		import sessions
		self.sessionStorage = sessions.SESSIONSTORAGE()
		try:
			import socket
			self.socket = socket
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.settimeout(0.0); self.sock.setblocking(0) # Set non-blocking
			self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		except: import traceback; traceback.print_exc()
	
	def bind(self):
		bound = False
		try:
			self.sock.bind( ("", self.address[1]) )
			bound = True
		except:
			import traceback; traceback.print_exc()
		return bound
	
	def getSession(self, ticket):
		if ticket in self.sessionStorage.sessions: return self.sessionStorage.sessions[ticket]
		else: return None
	
	########################################################################
	class CLIENTSOCK:
		def __init__(self, connection, timeout=10.0):
			self.timeout = timeout
			self.connection = connection
			self.sock, self.address = connection
			self.IP = self.address[0]
			import comms
			self.comms = comms
			self.instream = comms.STREAM()
			self.items = []
			self.outbuffer = ""
			self.timeoutClock = comms.TIMER()
		def run(self):
			# Handles stream/buffer IO, puts items (unpacked inbound packages) in items list.
			self.IO()
			items = self.items
			self.items = []
			return items, self.hasGoneStale()
		def IO(self):
			# RECEIVING (IN)
			try:
				data = self.sock.recv(1024)
				if data:
					self.instream.add(data)
					packages = self.instream.extract()
					items = self.comms.unpackList(packages)
					for item in items: self.items.append(item)
					self.timeoutClock.reset()
			except: pass
			# SENDING (OUT)
			try:
				if self.outbuffer:
					sent = self.sock.send(self.outbuffer)
					self.outbuffer = self.outbuffer[sent:]
			except: pass
		def send(self, data):
			try:
				self.outbuffer += self.comms.pack(data)
				if self.outbuffer:
					sent = self.sock.send(self.outbuffer)
					self.outbuffer = self.outbuffer[sent:]
			except: pass
		def hasGoneStale(self): # In other words, "hasTimedOut()".
			if self.timeoutClock.get() > self.timeout: return True
			else: return False
		def terminate(self):
			self.sock.close()
	########################################################################
	
	def run(self):
		parcels = []
		newConnections = []
		staleClients = []
		staleSessions = []
		
		newConnection = self.acceptNewConnection()
		if newConnection:
			clientSock = self.CLIENTSOCK(newConnection)
			ticket, session = self.sessionStorage.newSession(clientSock)
			#print("New connection from (%s), ticket=%s."%(clientSock.IP, ticket))
			newConnections.append( (clientSock.IP, ticket) )
		
		staleSessions = []
		for sessionTicket in self.sessionStorage.sessions:
			session = self.sessionStorage.sessions[sessionTicket]
			if session.clientSock:
				items, hasGoneStale = session.clientSock.run()
				for item in items:
					parcel = (sessionTicket, item)
					parcels.append(parcel)
				if hasGoneStale:
					#session.clientSock.terminate()
					#print("Client (%s) has gone stale."%(session.clientSock.IP))
					staleClients.append( (session.clientSock.IP, sessionTicket) )
					session.terminateClientSock()
					#session.clientSock = None
					#session.sessionTimeoutClock.reset()
			else:
				if session.hasGoneStale(): staleSessions.append(sessionTicket)
		
		for staleSession in staleSessions:
			self.sessionStorage.deleteSession(staleSession)
			#print("Session number %s went stale."%(staleSession))
			staleSessions.append( staleSession )
		
		return parcels, newConnections, staleClients, staleSessions
	
	def acceptNewConnection(self):
		try:
			self.sock.listen(1)
			client, address = self.sock.accept()
			client.settimeout(0.0); client.setblocking(0) # Set non-blocking
			return (client, address)
		except: pass
	
	def sendToAll(self, data):
		for sessionTicket in self.sessionStorage.sessions:
			session = self.sessionStorage.sessions[sessionTicket]
			if session.clientSock:
				session.clientSock.send(data)
	
	def sendTo(self, ticket, data):
		session = self.sessionStorage.sessions[ticket]
		session.clientSock.send(data)
	
	def terminate(self):
		# Terminate all sockets.
		for sessionTicket in self.sessionStorage.sessions:
			session = self.sessionStorage.sessions[sessionTicket]
			session.terminateClientSock()
		import socket
		self.sock.close()


###### ### ################################ ### ######
###### ### ### ------ TCP CLIENT ------ ### ### ######
###### ### ################################ ### ######

class TCP_CLIENT:

	def __init__(self, address, timeout=10.0):
		self.address = address
		import comms
		self.comms = comms
		self.instream = comms.STREAM()
		self.outbuffer = ""
		self.items = []
		self.timeoutClock = comms.TIMER()
		self.timeout = timeout
		import socket
		self.socket = socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.settimeout(0.0); self.sock.setblocking(0)
		self.CONNECTED = False
		self.CONNECTING = False
	
	def handleConnection(self):
		justConnected = False
		if not self.CONNECTED:
			if not self.CONNECTING:
				# We'll leave it to the higher level to initiate the connection when they want...
				#self.initiateConnection()
				pass
			else: # connection is in progress...
				connected, hasGoneStale = self.refreshConnectionStatus()
				if connected: justConnected = True
				if hasGoneStale: self.terminate()
		return justConnected
	
	def initiateConnection(self):
		try:
			self.sock.connect(self.address)
		except:
			pass
		self.timeoutClock.reset()
		self.CONNECTING = True
	
	def refreshConnectionStatus(self):
		hasGoneStale = False
		connected = False
		try:
			peer = self.sock.getpeername()
			if peer:
				connected = True
				self.CONNECTING = False
				self.CONNECTED = True
				self.timeoutClock.reset()
			else:
				hasGoneStale = self.hasGoneStale()
		except:
			pass
		return connected, hasGoneStale
			
	
	def run(self):
		justConnected = self.handleConnection()
				
		if self.CONNECTED:
			self.IO()
		items = self.items; self.items = []
		return items, self.hasGoneStale(), justConnected
	
	def IO(self):
		# RECEIVING (IN)
		try:
			data = self.sock.recv(1024)
			if data:
				self.instream.add(data)
				packages = self.instream.extract()
				items = self.comms.unpackList(packages)
				for item in items: self.items.append(item)
				self.timeoutClock.reset()
		except: pass
		# SENDING (OUT)
		try:
			if self.outbuffer:
				sent = self.sock.send(self.outbuffer)
				self.outbuffer = self.outbuffer[sent:]
		except: pass
	def send(self, data):
		try:
			self.outbuffer += self.comms.pack(data)
			if self.outbuffer:
				sent = self.sock.send(self.outbuffer)
				self.outbuffer = self.outbuffer[sent:]
		except: pass
	
	def hasGoneStale(self): # In other words, "hasTimedOut()".
		if self.timeoutClock.get() > self.timeout: return True
		else: return False
	def terminate(self):
		self.CONNECTING = False
		self.CONNECTION = False
		self.timeoutClock.reset()
		self.sock.close()




###### ### ################################ ### ######
###### ### ### ------ UDP SERVER ------ ### ### ######
###### ### ################################ ### ######

class UDP_SERVER:
	def __init__(self, address):
		self.address = address
		import socket
		self.socket = socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.settimeout(0.0); self.sock.setblocking(0)
	
	def bind(self):
		bound = False
		try: 
			self.sock.bind( ('', self.address[2]) )
			bound = True
		except: 
			import traceback; traceback.print_exc()
		return bound
	
	def run(self):
		basket = self.catch()
		return basket
	
	def catch(self):
		try:
			package, addr = self.sock.recvfrom(4096)
			import comms
			parcel = comms.unpack(package)
			return parcel, addr # This is a basket
		except:
			return None, None
	
	def throw(self, item, addr):
		import comms
		package = comms.packUDP(item)
		self.sock.sendto(package, addr)
	
	def terminate(self):
		self.sock.close()

###### ### ################################ ### ######
###### ### ### ------ UDP CLIENT ------ ### ### ######
###### ### ################################ ### ######

class UDP_CLIENT:
	def __init__(self, address):
		self.address = address
		import socket
		self.socket = socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def catch(self):
		try:
			package, addr = self.sock.recvfrom(4096)
			import comms
			item = comms.unpack(package)
			return item, addr
		except:
			return None, None
	
	def throw(self, ticket, item, addr):
		import comms
		parcel = (ticket, item)
		package = comms.packUDP(parcel)
		self.sock.sendto(package, addr)
	
	def terminate(self):
		self.sock.close()

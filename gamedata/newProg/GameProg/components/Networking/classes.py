### Networking Classes ###


###### ### ##################### ### ######
###### ### ### BASIC CLASSES ### ### ######
###### ### ##################### ### ######

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
		if ticket in self.sessionStorage.sessions:
			return self.sessionStorage.sessions[ticket]
		else:
			return None
	
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
			import socket
			try:
				self.sock.shutdown(socket.SHUT_RDWR)
			except:
				pass
			self.sock.close()
	########################################################################
	
	def run(self):
		bundles = []
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
					bundle = (sessionTicket, item)
					bundles.append(bundle)
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
		
		return bundles, newConnections, staleClients, staleSessions
	
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
		try:
			import socket
			self.sock.shutdown(socket.SHUT_RDWR)
		except:
			pass
		self.sock.close()






class UDP_SERVER:
	def __init__(self, address):
		import socket
		self.socket = socket
		self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.serverSock.bind(address)



class UDP_CLIENT:
	pass





###### ### #################### ### ######
###### ### ### HIGH CLASSES ### ### ######
###### ### #################### ### ######

class MS_SERVER:
	pass



class GPS_SERVER:
	"""
	WIP?
	"""
	def __init__(self, address="chasemoskal.dyndns.org:3201/3202", TCP_SERVER=None, UDP_SERVER=None):
	
		### Deciphering Addrs ###
		try:
			if not ':' in address:
				address = ':' + address
			host, ports = address.split(':')
			tcpPort, udpPort = ports.split('/')
			tcpAddr = host, tcpPort
			udpAddr = host, udpPort
			self.host = host
			self.tcpPort = tcpPort
			self.udpPort = udpPort
		except:
			print("\nThere was an error deciphering addrs (Networking/classes.GPS_SERVER.__init__).")
			import traceback
			traceback.print_exc()
		
		# Initiating Server
		try:
			self.tcpServer = TCP_SERVER(tcpAddr)
			self.udpServer = UDP_SERVER(udpAddr)
			print("Server is Initiated")
		except:
			print("\nThere was an error initiating the server (Networking/classes.GPS_SERVER.__init__).")
			import traceback
			traceback.print_exc()
	
	
	def run(self):
		# Accept new TCP clients
		newConnection = self.tcpServer.acceptNewConnection()
		if newConnection:
			newTcpClientHandler = TCP_CLIENT_HANDLER( newConnection )
			# Make it into a new session?
		







class MS_CLIENT:
	pass




class GPS_CLIENT:
	pass











###### ### ################### ### ######
###### ### ### SUB CLASSES ### ### ######
###### ### ################### ### ######
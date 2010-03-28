### Low-level Networking Classes ###


###### ### ################################ ### ######
###### ### ### ------ TCP SERVER ------ ### ### ######
###### ### ################################ ### ######

class TCP_SERVER:
	def __init__(self, address):
		self.shutdown = False
		self.active = False
		
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
			self.sock.bind(self.address)
			bound = True
			self.active = True
		except:
			import traceback; traceback.print_exc()
		return bound
	
	def getSession(self, ticket):
		if ticket in self.sessionStorage.sessions: return self.sessionStorage.sessions[ticket]
		else: return None
	
	########################################################################
	class CLIENTSOCK:
		def __init__(self, connection, timeout=10.0):
			self.active = True
			
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
		def send(self, item):
			try:
				self.outbuffer += self.comms.pack(item)
				if self.outbuffer:
					sent = self.sock.send(self.outbuffer)
					self.outbuffer = self.outbuffer[sent:]
			except: pass
		def hasGoneStale(self): # In other words, "hasTimedOut()".
			if self.timeoutClock.get() > self.timeout: return True
			else: return False
		def terminate(self):
			self.sock.close()
			self.active = False
	########################################################################
	
	def run(self):
		parcels = []
		newConnections = []
		staleConnections = []
		staleSessions = []
		clientsWhoLeft = []
		
		if not self.shutdown:
			newConnection = self.acceptNewConnection()
			if newConnection:
				clientSock = self.CLIENTSOCK(newConnection)
				ticket, session = self.sessionStorage.newSession(clientSock)
				#print("New connection from (%s), ticket=%s."%(clientSock.IP, ticket))
				newConnections.append( (clientSock.IP, ticket) )
		
		for ticket in self.sessionStorage.sessions:
			session = self.sessionStorage.sessions[ticket]
			if session.clientSock:
				items, hasGoneStale = session.clientSock.run()
				for item in items:
					flag, data = item
					parcel = (ticket, item)
					parcels.append(parcel)
					if flag == 'BYE': session.terminateClientSock(); clientsWhoLeft.append(ticket)
				if hasGoneStale:
					IP = session.clientSock.IP
					session.terminateClientSock()
					staleConnections.append( (IP, ticket) )
			else:
				if session.hasGoneStale(): staleSessions.append(ticket)
		
		for ticket in staleSessions:
			self.sessionStorage.deleteSession(ticket)
		
		if self.shutdown:
			clientSocks = self.countClientSocks()
			if clientSocks == 0:
				self.active = False
		
		return parcels, newConnections, staleConnections, staleSessions, clientsWhoLeft
	
	def countClientSocks(self):
		num = 0
		for ticket in self.sessionStorage.sessions:
			session = self.sessionStorage.sessions[ticket]
			if session.clientSock:
				num += 1
		return num
	
	def acceptNewConnection(self):
		try:
			self.sock.listen(1)
			client, address = self.sock.accept()
			client.settimeout(0.0); client.setblocking(0) # Set non-blocking
			return (client, address)
		except: pass
	
	def sendToAll(self, item):
		for ticket in self.sessionStorage.sessions:
			session = self.sessionStorage.sessions[ticket]
			if session.clientSock:
				session.clientSock.send(item)
	
	def sendTo(self, ticket, item):
		session = self.sessionStorage.sessions[ticket]
		session.clientSock.send(item)
	
	def startShutdown(self):
		"""
		Shutdown is how the tcpServer terminates.
		The shutdown process asks all clients to leave,
		and when they're all gone, the server terminates
		itself. active is False when the server should be
		deleted.
		"""
		self.sendToAll( ('BYE', 'BYE') )
		self.sock.close()
		self.shutdown = True # Start the shutdown.


###### ### ################################ ### ######
###### ### ### ------ TCP CLIENT ------ ### ### ######
###### ### ################################ ### ######

class TCP_CLIENT:

	def __init__(self, address, timeout=10.0):
		self.active = True # We start off active because we don't want to lose it right away.
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
		
		self.chkClock = comms.TIMER()
		self.nextCHK = 1
		self.CHK = 0
		
		self.connected = False
		self.connecting = False
	
	def refreshConnectionStatus(self):
		staleOnConnection = False
		justConnected = False
		try: peer = self.sock.getpeername()
		except: peer = None
		if peer:
			justConnected = True
			self.connecting = False
			self.connected = True
			self.timeoutClock.reset()
		else:
			staleOnConnection = self.hasGoneStale()
		return justConnected, staleOnConnection
	
	def initiateConnection(self):
		try: self.sock.connect(self.address)
		except: pass
		self.timeoutClock.reset()
		self.connecting = True
	
	def doCHK(self):
		if not self.CHK:
			if self.chkClock.get() > 2.0:
				self.CHK = self.nextCHK; self.nextCHK += 1
				self.send(('CHK', self.CHK))
				self.chkClock.reset()
	
	def run(self):
		items = []
		justConnected = False
		staleOnConnection = False
		gotShutdown = False
		hasGoneStale = False
		###
		if (not self.connected) and self.connecting:
			justConnected, staleOnConnection = self.refreshConnectionStatus()
			if staleOnConnection: self.terminate()
		if self.connected:
			items, gotShutdown = self.IO()
			if gotShutdown: self.terminate()
			hasGoneStale = self.hasGoneStale()
			if hasGoneStale: self.terminate()
		return items, justConnected, staleOnConnection, gotShutdown, hasGoneStale
	
	def IO(self):
		# RECEIVING (IN)
		items = []
		gotShutdown = False
		try:
			data = self.sock.recv(1024)
			if data:
				self.instream.add(data)
				packages = self.instream.extract()
				newItems = self.comms.unpackList(packages)
				for newItem in newItems:
					items.append(newItem)
					flag, data = newItem
					if flag == 'BYE':
						self.send(('BYE', 'BYE'))
						gotShutdown = True
					if flag == 'CHK':
						if data == self.CHK:
							self.CHK = 0
				self.timeoutClock.reset()
		except: pass
		# SENDING (OUT)
		try:
			self.doCHK()
			if self.outbuffer:
				sent = self.sock.send(self.outbuffer)
				self.outbuffer = self.outbuffer[sent:]
		except: pass
		return items, gotShutdown
	
	def send(self, item):
		try:
			self.outbuffer += self.comms.pack(item)
			if self.outbuffer:
				sent = self.sock.send(self.outbuffer)
				self.outbuffer = self.outbuffer[sent:]
		except: pass
	
	def hasGoneStale(self): # In other words, "hasTimedOut()".
		if self.timeoutClock.get() > self.timeout: return True
		else: return False
	
	def terminate(self):
		self.connected = False
		self.connecting = False
		self.timeoutClock.reset()
		self.sock.close()
		self.active = False




###### ### ################################ ### ######
###### ### ### ------ UDP SERVER ------ ### ### ######
###### ### ################################ ### ######

class UDP_SERVER:
	def __init__(self, address):
		self.active = False
		self.address = address
		import socket
		self.socket = socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.settimeout(0.0); self.sock.setblocking(0)
	
	def bind(self):
		bound = False
		try: 
			self.sock.bind(self.address)
			bound = True
			self.active = True
		except: 
			import traceback; traceback.print_exc()
		return bound
	
	def run(self):
		basket = self.catch()
		return basket
	
	def catch(self, max=10):
		# Returns a number of baskets
		baskets = []
		for i in range(max):
			try:
				package, addr = self.sock.recvfrom(4096)
				if package:
					import comms
					parcel = comms.unpack(package)
					basket = (parcel, addr)
					baskets.append(basket)
				else:
					break
			except:
				break
		return baskets
	
	def throw(self, item, addr):
		import comms
		package = comms.packUDP(item)
		self.sock.sendto(package, addr)
	
	def terminate(self):
		"""
		UDP Servers do not need to shutdown, they
		can just immediately terminate.
		"""
		self.sock.close()
		self.active = False

###### ### ################################ ### ######
###### ### ### ------ UDP CLIENT ------ ### ### ######
###### ### ################################ ### ######

class UDP_CLIENT:
	def __init__(self, address):
		self.address = address
		import socket
		self.socket = socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.settimeout(0.0); self.sock.setblocking(0)

	def catch(self, max=10):
		items = []
		for i in range(max):
			try:
				package, addr = self.sock.recvfrom(4096)
				if package:
					import comms
					item = comms.unpack(package)
					items.append(item)
				else:
					break
			except:
				break
		return items
	
	def throw(self, parcel):
		import comms
		package = comms.packUDP(parcel)
		self.sock.sendto(package, self.address)
	
	def terminate(self):
		self.sock.close()

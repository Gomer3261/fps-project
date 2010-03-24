###### ### #################### ### ######
###### ### ### CORE CLASSES ### ### ######
###### ### #################### ### ######

# When a client connects to the gameplay server,
# the server will send a GREET item, which gives them their ticket,
# and the host's UID.
# The client will reply with an AU item, which requests
# the creation of a user registered for their ticket with their
# user name in the GameState.
# The Server should then reply to the AU item with a UID item,
# which tells the client their new UID.
# A FAIL item indicates something went wrong, and the client should
# disconnect and perhaps try again.

class GPS:
	import classes
	import comms
	def __init__(self, addressString="192.168.1.100:3200/3201"):
		self.shutdown = False
		self.active = False
		
		self.addressString = addressString
		self.addressTuple = self.comms.makeAddressTuple(addressString)
		host, tcpPort, udpPort = self.addressTuple
		tcpAddress = ("", tcpPort)
		udpAddress = ("", udpPort)
		
		# Initiating Server
		self.tcpServer = self.classes.TCP_SERVER(tcpAddress)
		self.udpServer = self.classes.UDP_SERVER(udpAddress)
	
	def bind(self):
		serverSuccess = False
		tcpBound = self.tcpServer.bind()
		udpBound = self.udpServer.bind()
		if tcpBound and udpBound:
			serverSuccess = True
			self.active = True
		return serverSuccess
	
	def associateUser(self, ticket, UID):
		self.tcpServer.getSession(ticket).UID = UID
	
	def getUIDByTicket(self, ticket):
		return self.tcpServer.getSession(ticket).UID
	
	def getUdpAddrByTicket(self, ticket):
		return self.tcpServer.getSession(ticket).udp
		
	def run(self, Admin, GameState, Interface):
		allParcels = [] # We will return this at the end
		
		parcels = self.runTcpServer(Admin, GameState, Interface)
		for parcel in parcels: allParcels.append(parcel)
		
		parcels = self.runUdpServer(Interface)
		for parcel in parcels: allParcels.append(parcel)
		
		if (not self.tcpServer) and (not self.udpServer): self.active = False
		
		return allParcels
	
	def runTcpServer(self, Admin, GameState, Interface):
		allParcels = []
		### TCP SERVER ###
		if self.tcpServer:
			parcels, newConnections, staleClients, staleSessions = self.tcpServer.run()
			for parcel in parcels:
				ticket, item = parcel
				flag, data = item
				if flag == 'CHK': # This is a check.
					Interface.out("Server: TCP CHK handled.")
					self.send(ticket, item) # We echo those back.
				if flag == 'AU': # Add User Request (to the GameState)
					Interface.out("Server: Got AU")
					name = data
					UID = GameState.addUser(ticket, name)
					self.send(ticket, ('UID', UID))
					Interface.out("Server: Sent UID")
				allParcels.append(parcel)
			for newConnection in newConnections:
				IP, ticket = newConnection
				Interface.out("Server: New connection, %s, %s."%(IP, ticket))
				self.send(ticket, ('GREET', (ticket, Admin.UID)))
				Interface.out("Server: Sent GREET")
			for staleClient in staleClients:
				Interface.out("Server: A client went stale.")
			for staleSession in staleSessions:
				Interface.out("Server: A session went stale.")
			
			if not self.tcpServer.active: self.tcpServer=None; Interface.out("Server: TCP server terminated.", console=True)
		###
		return allParcels
	
	def runUdpServer(self, Interface):
		parcels = []
		### UDP SERVER ###
		if self.udpServer:
			baskets = self.udpServer.run()
			for basket in baskets:
				parcel, addr = basket
				ticket, item = parcel
				flag, data = item
				if flag == 'CHK':
					Interface.out("Server: UDP CHK handled.")
					self.udpServer.throw(item, addr) # echoing the check back
				### Checking for new TCP/UDP Associations ###
				session = self.tcpServer.getSession(ticket)
				if session:
					if not session.udp: Interface.out("Server: UDP associated with ticket %s"%ticket, console=True)
					session.udp = addr
					parcels.append(parcel)
				else: Interface.out("Server: Error, Network/core, UDP message specified non-existant session... O_o", console=True)
			
			if not self.udpServer.active: self.udpServer=None; Interface.out("Server: UDP server terminated.", console=True)
		###
		return parcels
	
	def send(self, ticket, item):
		self.tcpServer.sendTo(ticket, item)
	
	def throw(self, ticket, item):
		addr = self.getUdpAddrByTicket(ticket); self.udpServer.throw(item, addr)
	
	def startShutdown(self):
		self.tcpServer.startShutdown() # TCP servers need to be shutdown first.
		self.udpServer.terminate() # UDP servers can be instantly terminated.
		self.shutdown = True
			

class GPC:
	import classes
	import comms
	def __init__(self, addressString="192.168.1.100:3200/3201"):
		self.active = True
		
		self.addressString = addressString
		self.addressTuple = self.comms.makeAddressTuple(addressString)
		host, tcpPort, udpPort = self.addressTuple
		tcpAddress = ("", tcpPort)
		udpAddress = ("", udpPort)
		
		self.tcpClient = self.classes.TCP_CLIENT(tcpAddress)
		self.udpClient = self.classes.UDP_CLIENT(udpAddress)
		self.ticket = 0
		self.hostUID = 0
	
	def initiateConnection(self):
		self.tcpClient.initiateConnection()
	
	def send(self, item):
		self.tcpClient.send(item)
	
	def throw(self, item):
		if self.ticket:
			self.udpClient.throw( (self.ticket, item) )
		else:
			print("GPC: Cannot throw; did not obtain ticket yet.")
	
	def run(self, Admin, Interface):
		bundles = self.runTcp(Admin, Interface)
		udpBundles = self.runUdp(Admin, Interface)
		for udpBundle in udpBundles: bundles.append(udpBundle)
		return bundles
	
	def runTcp(self, Admin, Interface):
		bundles = []
		if self.tcpClient:
			items, justConnected, staleOnConnection, gotShutdown, hasGoneStale = self.tcpClient.run()
			for item in items:
				flag, data = item
				###
				if flag == 'GREET':
					Interface.out("Client: Got GREET.")
					self.ticket, self.hostUID = data
					self.send( ('AU', Admin.getGameInfo()['username']) )
					self.throw( ('X', 0) )
					Interface.out("Client: Sent AU and threw X.")
				if flag == "UID":
					Interface.out("Client: Got UID")
					Admin.UID = data
				###
				if self.hostUID:
					bundles.append( (self.hostUID, item) )
			if justConnected: Interface.out("Client: We just connected as a client to the server!")
			if staleOnConnection: Interface.out("Client: Failed to connect to host: %s"%self.addressString)
			if gotShutdown: Interface.out("Client: The server has shut down the connection.")
			if hasGoneStale: Interface.out("Client: Connection to the server just went stale.")
			if not self.tcpClient.active:
				self.terminate()
		return bundles
	
	def runUdp(self, Admin, Interface):
		bundles = []
		if self.udpClient:
			items = self.udpClient.catch()
			for item in items:
				bundles.append( (self.hostUID, item) )
		return bundles
			
	
	def terminate(self):
		self.tcpClient = None
		self.udpClient.terminate(); self.udpClient = None
		self.active = False




class MS_SERVER:
	pass




class MS_CLIENT:
	pass



###### ### #################### ### ######
###### ### ### CORE CLASSES ### ### ######
###### ### #################### ### ######

class GPS:
	import classes
	def __init__(self, address=("IP", 3200, 3201)):
		self.shutdown = False
		self.active = False
		
		# Initiating Server
		self.tcpServer = self.classes.TCP_SERVER(address)
		self.udpServer = self.classes.UDP_SERVER(address)
	
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
		
	def run(self, Interface):
		allParcels = [] # We will return this at the end
		
		parcels = self.runTcpServer(Interface)
		for parcel in parcels: allParcels.append(parcel)
		
		parcels = self.runUdpServer(Interface)
		for parcel in parcels: allParcels.append(parcel)
		
		if (not self.tcpServer) and (not self.udpServer): self.active = False
		
		return allParcels
	
	def runTcpServer(self, Interface):
		parcels = []
		### TCP SERVER ###
		if self.tcpServer:
			parcels, newConnections, staleClient, staleSessions = self.tcpServer.run()
			for parcel in parcels:
				ticket, item = parcel
				flag, data = item
				if flag == 'CHK': # This is a check.
					self.tcpServer.sendTo(ticket, item) # We echo those back.
				else:
					allParcels.append(parcel)
			
			if not self.tcpServer.active: self.tcpServer=None; Interface.out("TCP server terminated.", console=True)
		###
		return parcels
	
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
					self.udpServer.throw(item, addr) # echoing the check back
				### Checking for new TCP/UDP Associations ###
				session = self.tcpServer.getSession(ticket)
				if session:
					if not session.udp: Interface.out("UDP associated with ticket %s"%ticket, console=True)
					session.udp = addr
					parcels.append(parcel)
				else: Interface.out("Error, Network/core, UDP message specified non-existant session... O_o", console=True)
			
			if not self.udpServer.active: self.udpServer=None; Interface.out("UDP server terminated.", console=True)
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
	pass

		




class MS_SERVER:
	pass




class MS_CLIENT:
	pass



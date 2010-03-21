###### ### #################### ### ######
###### ### ### CORE CLASSES ### ### ######
###### ### #################### ### ######

class GPS:
	"""
	WIP?
	"""
	import classes
	def __init__(self, address=("IP", 3200, 3201)):
		self.SHUTDOWN = False
		self.TERMINATED = False
		
		# Initiating Server
		self.tcpServer = self.classes.TCP_SERVER(address)
		self.udpServer = self.classes.UDP_SERVER(address)
	
	def bind(self):
		serverSuccess = False
		tcpBound = self.tcpServer.bind()
		udpBound = self.udpServer.bind()
		if tcpBound and udpBound:
			serverSuccess = True
		return serverSuccess
	
	def associateUser(self, ticket, UID):
		session = self.tcpServer.getSession(ticket)
		session.UID = UID
	
	def getUIDByTicket(self, ticket):
		session = self.tcpServer.getSession(ticket)
		return session.UID
		
	
	def run(self, Interface):
		allParcels = [] # We will return this at the end
		
		### TCP SERVER ###
		if self.tcpServer:
			parcels, newConnections, staleClient, staleSessions, terminated = self.tcpServer.run()
			for parcel in parcels:
				ticket, item = parcel
				flag, data = item
				if flag == 'CHK': # This is a check.
					self.tcpServer.sendTo(ticket, item) # We echo those back.
				else:
					allParcels.append(parcel)
			if terminated:
				self.tcpServer = None
				self.TERMINATED = True
		###
		
		### UDP SERVER ###
		if self.udpServer:
			basket = self.udpServer.run()
			if basket:
				parcel, addr = basket
				ticket, item = parcel
				flag, data = item
				if flag == 'CHK':
					self.udpServer.throw(item, addr) # echoing the check back
				### Checking for new TCP/UDP Associations ###
				session = self.tcpServer.getSession(ticket)
				if session:
					if not session.udp: print("UDP associated with ticket %s"%ticket)
					session.udp = addr
					allParcels.append(parcel)
				else: print("Error, Network/core, UDP message specified non-existant session... O_o")
		###
		
		return allParcels, self.TERMINATED
	
	def shutdown(self):
		self.tcpServer.shutdown() # TCP servers need to be shutdown first.
		self.udpServer.terminate() # UDP servers can be instantly terminated.
		self.udpServer = None
		self.SHUTDOWN = True
			

class GPC:
	pass

		




class MS_SERVER:
	pass




class MS_CLIENT:
	pass



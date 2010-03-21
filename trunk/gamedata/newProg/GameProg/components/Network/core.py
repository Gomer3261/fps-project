###### ### #################### ### ######
###### ### ### HIGH CLASSES ### ### ######
###### ### #################### ### ######

class GP_SERVER:
	"""
	WIP?
	"""
	def __init__(self, address=("IP", 3200, 3201)):
		# Initiating Server
		self.tcpServer = TCP_SERVER(tcpAddr)
		self.udpServer = UDP_SERVER(udpAddr)
	
	def bind(self):
		serverSuccess = False
		tcpBound = self.tcpServer.bind()
		udpBound = self.udpServer.bind()
		if tcpBound and udpBound:
			serverSuccess = True
		return serverSuccess
	
	def run(self, GameState, Interface):
		newInItems = []
		
		bundles, newConnections, staleClient, staleSessions = self.tcpServer.run()
		for bundle in bundles:
			ticket, item = bundle
			flag, data = item
			if flag == 'CHK': # This is a check.
				self.tcpServer.sendTo(ticket, item) # We echo those back.
			else:
				newInItems.append(item)
		
		baskets = self.udpServer.run()
		for basket in baskets:
			item, addr = basket
			flag, data = item
			if flag == 'CHK':
				self.udpServer.throw(item, addr) # echoing the check back

class GPS_CLIENT:
	pass

		




class MS_SERVER:
	pass




class MS_CLIENT:
	pass



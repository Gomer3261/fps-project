class Class:
	def __init__(self):
		import time; self.time = time
		import comms; self.comms = comms
		
		self.reportOutInterval = 1.0
		self.reportOutClock = comms.TIMER()
		
		self.resetIO()
	
	def resetIO(self):
		self.sentBytesTCP = 0
		self.receivedBytesTCP = 0
		self.sentBytesUDP = 0
		self.receivedBytesUDP = 0
	
	def reportIn(self, GPS, GPC):
		if GPS:
			self.sentBytesTCP += GPS.tcpServer.sentBytes; GPS.tcpServer.sentBytes = 0
			self.sentBytesUDP += GPS.udpServer.sentBytes; GPS.udpServer.sentBytes = 0
			self.receivedBytesTCP += GPS.tcpServer.receivedBytes; GPS.tcpServer.receivedBytes = 0
			self.receivedBytesUDP += GPS.udpServer.receivedBytes; GPS.udpServer.receivedBytes = 0
		
		if GPC:
			self.sentBytesTCP += GPC.tcpClient.sentBytes; GPC.tcpClient.sentBytes = 0
			self.sentBytesUDP += GPC.udpClient.sentBytes; GPC.udpClient.sentBytes = 0
			self.receivedBytesTCP += GPC.tcpClient.receivedBytes; GPC.tcpClient.receivedBytes = 0
			self.receivedBytesUDP += GPC.udpClient.receivedBytes; GPC.udpClient.receivedBytes = 0
	
	def run(self):
		if self.reportOutClock.get() > self.reportOutInterval:
			self.reportOutClock.reset()
		
			tcpUpload = (self.sentBytesTCP/self.reportOutInterval)/1024
			tcpDownload = (self.receivedBytesTCP/self.reportOutInterval)/1024
			udpUpload = (self.sentBytesUDP/self.reportOutInterval)/1024
			udpDownload = (self.receivedBytesUDP/self.reportOutInterval)/1024
			self.resetIO()
			
			tcpRates = tcpUpload, tcpDownload
			udpRates = udpUpload, udpDownload
			
			self.reportOut(tcpRates, udpRates)
	
	def reportOut(self, tcpRates, udpRates):
		print("TCP:", tcpRates)
		print("UDP:", udpRates)

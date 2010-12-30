class initiateServer:
	def __init__(self, port):
		self.port=port
		
		import socket
		self.buf=1024
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setblocking(0)
		self.sock.bind(('',port))
		
		import netcom; self.netcom = netcom
		
		self.connections = {} # Dictionary of connections
		
		import time; self.time=time
		self.lastIntervalExecution = 0.0
		
		self.nextId=1
	def getId(self): id=self.nextId; self.nextId+=1; return id
		
	def handleNetBundle(self, bundle):
		packet, addr = bundle
		flag = packet[1]
		data = packet[2:]
		
		if flag == "c": # Connection Request.
			username = data
			id = self.getId()
			self.sock.sendto(self.netcom.codes['net']+'a'+str(id),addr) # Acknowledged/Accepted!
			self.connections[id] = {} #{'username':username, 'addr':addr}
			self.connections[id]['addr'] = addr
			self.connections[id]['username'] = username
			self.connections[id]['lastThrowSeq'] = 0
			self.connections[id]['nextThrowSeq'] = 1
			print("user connected: "+username+", id: "+str(id))
	
	
	def recvBundles(self, max=10):
		bundles = []
		for i in range(max):
			try:
				bundle = self.sock.recvfrom(self.buf)
				bundles.append(bundle)
			except: break
		return bundles
	
	def throw(self, data, id):
		packet=self.netcom.serverBuildThrowPacket(self.connections[id]['nextThrowSeq'], data)
		self.sock.sendto(packet, self.connections[id]['addr'])
		self.connections[id]['nextThrowSeq']+=1
	
	def throwToAll(self, data):
		for id in self.connections:
			addr = self.connections[id]['addr']
			self.sock.sendto(packet, addr)
			self.connections[id]['nextThrowSeq']+=1
	
	def interval(self, function, argument, period):
		if self.time.time() - self.lastIntervalExecution > period:
			function( argument )
			self.lastIntervalExecution = self.time.time()
	
	def mainloop(self, gamestate):
		for bundle in self.recvBundles():
			packet, addr = bundle
			if packet: print('packet: '+packet)
			
			if packet[0] == self.netcom.codes['net']:
				self.handleNetBundle(bundle)
			
			if packet[0] == self.netcom.codes['throw']:
				seq, id, data = self.netcom.serverParseThrowPacket(packet)
				if data and seq > self.connections[id]['lastThrowSeq']:
					self.connections[id]['lastThrowSeq'] = seq
					print("throw in: "+data)
			
			if packet[0] == self.netcom.codes['stream']:
				pass
			








#Server = initiateServer(3205)
#print("Server initiated and running.")
#while True:
#	Server.mainloop()
class initializeClient:
	def __init__(self, addr, username):
		self.addr=addr; self.username=username
		
		# We use engine to communicate current id
		import engine; self.engine=engine
		
		import socket
		self.buf=1024
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setblocking(0)
		
		from . import netcom; self.netcom = netcom
		#import netcom; self.netcom = netcom
		
		import time; self.time=time
		self.lastConnectionAttempt = 0.0
		self.connectionAttemptPeriod = 0.5 # will attempt every 0.5 seconds.
		self.connectionAttempts=0
		self.connected = False
		
		self.timeout = 5.0 # must be greater than 3 seconds
		self.lastContact = self.time.time()
		self.lastKeepAlive = self.time.time()
		
		self.lastInterval = 0.0
		
		self.lastThrowSeq = 0
		self.nextThrowSeq = 1
	
	def isConnected(self):
		return self.connected
	
	def handleNetBundle(self, flag, payload, addr):
		if flag == 1: # CONNECTION ACCEPTED!
			self.engine.id = payload
			self.connected = True
			self.lastContact = self.time.time()
			print('HANDSHAKE SUCCESS, given id: ',payload)
		
		if flag == 2: # Keep Alive Packet
			print('netin: keepalive')
			if self.connected:
				self.lastContact = self.time.time()
			else:
				self.engine.id = payload
				self.connected = True
				self.lastContact = self.time.time()
				print('MISSED CONNECTION PACKET, INDIRECTLY CONNECTED VIA KEEP ALIVE PACKET, given id: ',payload)
	
	
	
	def recvBundles(self, max=10):
		bundles = []
		for i in range(max):
			try:
				packet, addr = self.sock.recvfrom(self.buf)
				if packet: bundles.append( (packet, addr) )
			except: break
		return bundles
	
	
	
	
	def throw(self, payload):
		packet = self.netcom.pack( (1,self.nextThrowSeq,self.engine.id,payload) )
		self.sock.sendto(packet, self.addr)
		self.nextThrowSeq+=1
	
	
	def interval(self, function, argument, period):
		if self.time.time() - self.lastInterval > period:
			function( argument )
			self.lastInterval = self.time.time()
	
	
	def mainloop(self, gamestate):
		inDeltas = []
		
		for bundle in self.recvBundles():
			self.lastContact = self.time.time()
			packet, addr = bundle
			data = self.netcom.unpack(packet)
			type=data[0]
			
			#print("DATA IN:")
			#print(data)
			#print(addr)
			
			if type == 0: # NET PACKET
				type, flag, payload = data
				self.handleNetBundle(flag, payload, addr)
			
			if type == 1: # THROW PACKET
				type, seq, payload = data
				if payload and seq > self.lastThrowSeq:
					self.lastThrowSeq = seq
					inDeltas.append(payload)
			
			if type == 2: # STREAM PACKET
				pass
		
		if not self.connected:
			if self.time.time()-self.lastConnectionAttempt > self.connectionAttemptPeriod:
				print("attempting handshake...")
				request = self.netcom.pack( (0, 1, self.username) )
				self.sock.sendto(request, self.addr)
				self.lastConnectionAttempt = self.time.time()
				self.connectionAttempts+=1
		else: # We are connected.
			if self.time.time() - self.lastContact > self.timeout:
				# We've lost connection.
				self.connectionAttempts=0
				self.connected = False
			else:
				# We haven't lost connection.
				if self.time.time() - self.lastKeepAlive > ((self.timeout/2)-1.0):
					# One second before half the time it takes to timeout, we send a keepalive thingy.
					self.sock.sendto( self.netcom.pack((0, 2, self.engine.id)), self.addr )
					self.lastKeepAlive = self.time.time()
		
		return inDeltas



#Client = initializeClient( ('192.168.1.101', 3203), "Jimmy" )
#print("Client initiated and running.")
#import time
#lastThrow = 0.0
#while True:
#	Client.mainloop(None)
#	if Client.connected:
#		if time.time()-lastThrow > 1.0:
#			Client.throw("OLIOLIO!")
#			lastThrow = time.time()

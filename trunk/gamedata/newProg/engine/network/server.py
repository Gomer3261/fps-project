class initializeServer:
	def __init__(self, port):
		self.port=port
		
		import socket
		self.buf=1024
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(('',port))
		self.sock.setblocking(0)
		
		print("SERVER RUNNING ON PORT "+str(port))
		
		from . import netcom; self.netcom = netcom
		self.throwHandler = netcom.createServerThrowHandler()
		
		self.connections = {} # Dictionary of connections
		
		self.gamestate=None
		
		import time; self.time=time
		self.lastInterval = 0.0
		self.timeout = 5.0
		self.lastKeepAlive = self.time.time()
	
	def isConnected(self):
		return (len(self.connections) > 0)
		
	def handleNetBundle(self, flag, payload, addr, gamestate):
		if flag == 1: # Connection Request.
			username = payload
			id = gamestate.addUser( username ) # Adding user to gamestate, and getting their id.
			self.sock.sendto( self.netcom.pack((0,1,id)), addr ) # Acknowledged/Accepted!
			self.connections[id] = {} #{'username':username, 'addr':addr}
			self.connections[id]['addr'] = addr
			self.connections[id]['username'] = username
			self.connections[id]['lastThrowSeq'] = 0
			self.connections[id]['nextThrowSeq'] = 1
			self.connections[id]['lastContact'] = self.time.time()
			print("USER CONNECTED: "+username+", given id: "+str(id))
		
		if flag == 2: # Keep Alive packet
			id = payload
			self.connections[id]['lastContact'] = self.time.time()
	
	def recvBundles(self, max=10):
		bundles = []
		for i in range(max):
			try:
				packet, addr = self.sock.recvfrom(self.buf)
				if packet: bundles.append( (packet, addr) )
			except: break
		return bundles
	
	def throw(self, payload, id):
		seq = self.connections[id]['nextThrowSeq']
		packet = self.netcom.pack( (1,seq,payload) )
		self.sock.sendto( packet, self.connections[id]['addr'] )
		self.connections[id]['nextThrowSeq']+=1
	
	def throwToAll(self, payload):
		for id in self.connections:
			self.throw(payload, id)
	
	def interval(self, function, argument, period):
		if self.time.time() - self.lastInterval > period:
			function( argument )
			self.lastInterval = self.time.time()
	
	def timeoutLoop(self, gamestate):
		toRemove = []
		for id in self.connections:
			c = self.connections[id]
			if self.time.time() - c['lastContact'] > self.timeout:
				toRemove.append(id)
		for id in toRemove:
			del self.connections[id]
			gamestate.removeUser(id) # Removing user from the GameState.
			print("USER "+str(id)+" DISCONNECTED. They timed out.")
	
	def keepAliveLoop(self):
		# We haven't lost connection.
		if self.time.time() - self.lastKeepAlive > ((self.timeout/2)-1.0):
			# One second before half the time it takes to timeout, we send a keepalive thingy.
			for id in self.connections:
				addr = self.connections[id]['addr']
				self.sock.sendto( self.netcom.pack((0, 2, id)), addr )
				self.lastKeepAlive = self.time.time()				
	
	def mainloop(self, gamestate):
		self.timeoutLoop(gamestate) # Removes connections who have stuck around for too long.
		self.keepAliveLoop()
		
		inDeltas = []
		for bundle in self.recvBundles():
			packet, addr = bundle
			data = self.netcom.unpack(packet)
			type=data[0]
			
			#print("DATA IN:")
			#print(data)
			#print(addr)
			
			if type == 0: # NET PACKET
				type, flag, payload = data
				self.handleNetBundle(flag, payload, addr, gamestate)
			
			if type == 1: # THROW PACKET
				type, seq, id, payload = data
				self.connections[id]['lastContact'] = self.time.time() # refreshing the lastContact to keep client from timing out.
				if payload and seq > self.connections[id]['lastThrowSeq']:
					self.connections[id]['lastThrowSeq'] = seq
					inDeltas.append(payload)
			
			if type == 2: # STREAM PACKET
				pass
		
		return inDeltas
			








#Server = initializeServer(3203)
#print("Server initiated and running.")
#while True:
#	Server.mainloop(None)
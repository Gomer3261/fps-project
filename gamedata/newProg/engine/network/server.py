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
		#import netcom; self.netcom=netcom
		
		self.connections = {} # Dictionary of connections
		
		import time; self.time=time
		self.lastInterval = 0.0
		
		self.nextId=1
	def getId(self): id=self.nextId; self.nextId+=1; return id
		
	def handleNetBundle(self, flag, payload, addr):
		if flag == 1: # Connection Request.
			username = payload
			id = self.getId()
			self.sock.sendto( self.netcom.pack((0,1,id)), addr ) # Acknowledged/Accepted!
			self.connections[id] = {} #{'username':username, 'addr':addr}
			self.connections[id]['addr'] = addr
			self.connections[id]['username'] = username
			self.connections[id]['lastThrowSeq'] = 0
			self.connections[id]['nextThrowSeq'] = 1
			print("USER CONNECTED: "+username+", given id: "+str(id))
	
	
	def recvBundles(self, max=10):
		bundles = []
		for i in range(max):
			try:
				bundle = self.sock.recvfrom(self.buf)
				bundles.append(bundle)
			except: break
		return bundles
	
	def throw(self, payload, id):
		seq = self.connections[id]['nextThrowSeq']
		self.sock.sendto( self.netcom.pack((1,seq,payload)), self.connections[id]['addr'] )
		self.connections[id]['nextThrowSeq']+=1
	
	def throwToAll(self, payload):
		for id in self.connections:
			self.throw(payload, id)
	
	def interval(self, function, argument, period):
		if self.time.time() - self.lastInterval > period:
			function( argument )
			self.lastInterval = self.time.time()
	
	def mainloop(self, gamestate):
		inDeltas = []
		for bundle in self.recvBundles():
			packet, addr = bundle
			data = self.netcom.unpack(packet)
			type=data[0]
			
			print("DATA IN:")
			print(data)
			print(addr)
			
			if type == 0: # NET PACKET
				print("net packet")
				type, flag, payload = data
				self.handleNetBundle(flag, payload, addr)
			
			if type == 1: # THROW PACKET
				print("throw packet")
				type, seq, id, payload = data
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
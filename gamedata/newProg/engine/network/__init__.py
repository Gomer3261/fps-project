import time;
lastGamestateDataSend = 0.0

remoteHandler=None
class REMOTE_HANDLER:
	def __init__(self, addr):
		self.addr		= addr
		self.buf		= 1024
		self.timeout	= 5.0
		import time; self.time=time
		import engine; self.engine=engine
		from . import netcom; self.netcom=netcom
		self.lastKeepAlive=0.0
		self.initialize()
	
	def recv(self, max=10):
		bundles = []
		for i in range(max):
			try:
				packet, addr = self.sock.recvfrom(self.buf)
				if packet: bundles.append( (packet, addr) )
			except: break
		return bundles



class createServer(REMOTE_HANDLER):
	def initialize(self):
		import socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		self.sock.bind( ('',self.addr[1]) )
		self.sock.setblocking(0)
		print("SERVER RUNNING:", self.addr)
		self.connections = {}
	
	def throw(self, item, id):
		self.connections[id].throw(item)
	def throwToAll(self, item):
		for id in self.connections:
			self.connections[id].throw(item)
	
	def main(self, gamestate):
		self.timeoutLoop(gamestate) # Gamestate users are removed on timeouts.
		self.keepAliveLoop()
		
		inItems = []
		for bundle in self.recv():
			packet, addr = bundle
			data = self.netcom.unpack(packet)
			type=data[0]
			
			if type==0: # NET Packet
				type, flag, payload = data
				gamestateUsersToAdd = self.handleNetPacket(flag, payload, addr, gamestate)
			if type==1: # THROW Packet
				type, seq, label, id, payload = data
				connection = self.connections[id]; connection.contact()
				items = connection.handleThrowPacket(seq, label, id, payload)
				for item in items: inItems.append(item)
			if type==2: # STREAM Packet
				pass
		return inItems
	
	def handleNetPacket(self, flag, payload, addr, gamestate):
		if flag == 1: # Connection Request.
			username = payload
			id = gamestate.addUser( username )
			reply = (0, 1, id)
			self.sock.sendto( self.netcom.pack(reply),addr )
			self.connections[id] = self.netcom.createConnection(self, addr, id, username)
			print("USER CONNECTED: "+username+", given id: "+str(id))
		elif flag == 2: # Keep Alive Packet
			self.connections[payload].contact()
	
	def keepAliveLoop(self):
		if self.time.time()-self.lastKeepAlive > ((self.timeout/2)-1.0):
			for id in self.connections:
				c=self.connections[id]; item=(0, 2, id)
				self.sock.sendto( self.netcom.pack(item), c.addr )
				self.lastKeepAlive = self.time.time()
	
	def timeoutLoop(self, gamestate):
		toRemove = []
		for id in self.connections:
			connection = self.connections[id]
			if connection.hasGoneStale():
				toRemove.append(id)
		for id in toRemove:
			del self.connections[id]
			gamestate.removeUser(id) # Removing the user from the GameState
			print("USER "+str(id)+" DISCONNECTED. They timed out.")
	
	
	

class createClient(REMOTE_HANDLER):
	def initialize(self):
		import socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setblocking(0)
		
		self.lastConnectionAttempt=0.0 # time of last connection attempt
		self.connectionAttemptPeriod=0.5 # time between connection attempts
		self.connectionAttempts=0 # connection attempts in a row
		self.connection = None # when connected, this is a connection object.
	
	def throw(self, item):
		self.connection.throw(item)
	
	def main(self, gamestate): # we don't actually use gamestate, it's because the server's main needs it.
		if not self.connection: self.attemptConnection()
		else:
			self.keepAliveLoop()
			if self.connection.hasGoneStale():
				self.connectionAttempts=0; self.connection=None
				print("DISCONNECTED! SERVER TIMED OUT.")
		
		inItems = []
		for bundle in self.recv():
			packet, addr = bundle
			data = self.netcom.unpack(packet)
			type=data[0]
			
			if type==0: # NET PACKET
				type, flag, payload = data
				self.handleNetPacket(flag, payload)
			elif type==1: # THROW PACKET
				type, seq, label, id, payload = data
				items = self.connection.handleThrowPacket(seq, label, id, payload)
				for item in items: inItems.append(item)
			elif type==2: # STREAM PACKET
				pass
		return inItems
	
	def keepAliveLoop(self):
		if self.time.time()-self.lastKeepAlive > ((self.timeout/2)-1.0):
			item=(0, 2, self.engine.id)
			self.sock.sendto( self.netcom.pack(item), self.addr )
			self.lastKeepAlive = self.time.time()
	
	def handleNetPacket(self, flag, payload):
		if flag == 1: # Connection Accepted
			self.engine.id = payload
			self.connection = self.netcom.createConnection(self, self.addr)
			print("CONNECTION SUCCESS, given id:", payload)
		elif flag == 2: # Keep Alive Packet
			if self.connection: self.connection.contact()
			else:
				self.engine.id=payload
				self.connection=self.netcom.createConnection(self, self.addr)
				print("INDIRECTLY CONNECTED VIA KEEP ALIVE PACKET, given id:", payload)
	
	def attemptConnection(self):
		if self.time.time()-self.lastConnectionAttempt > self.connectionAttemptPeriod:
			self.lastConnectionAttempt = self.time.time(); self.connectionAttempts+=1
			print("requesting connection... "+str(self.connectionAttempts))
			request = (0, 1, self.engine.username)
			self.sock.sendto(self.netcom.pack(request),self.addr)


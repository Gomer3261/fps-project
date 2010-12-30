class initializeClient:
	def __init__(self, addr, username):
		self.addr=addr; self.username=username
		
		# We use engine to communicate current id
		#import engine; self.engine=engine
		class ENGINE:
			def __init__(self): self.id=1
		self.engine=ENGINE()
		
		import socket
		self.buf=1024
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setblocking(0)
		
		#from . import netcom; self.netcom = netcom
		import netcom; self.netcom = netcom
		
		import time; self.time=time
		self.lastConnectionAttempt = 0.0
		self.connectionAttemptPeriod = 0.5 # will attempt every 0.5 seconds.
		self.connectionAttempts=0
		self.connected = False
		
		self.lastInterval = 0.0
		
		self.lastThrowSeq = 0
		self.nextThrowSeq = 1
	
	def handleNetBundle(self, bundle):
		packet, addr = bundle
		flag = packet[1]
		data = packet[2:]
		
		if flag == "a":
			id = int(data)
			self.engine.id = id
			self.connected = True
			print('handshake success, id: '+data)
	
	
	
	def recvBundles(self, max=10):
		bundles = []
		for i in range(max):
			try:
				bundle = self.sock.recvfrom(self.buf)
				bundles.append(bundle)
			except: break
		return bundles
	
	
	
	
	def throw(self, data):
		packet=self.netcom.clientBuildThrowPacket(self.nextThrowSeq, self.engine.id, data)
		self.sock.sendto(packet, self.addr)
		self.nextThrowSeq+=1
	
	
	def interval(self, function, argument, period):
		if self.time.time() - self.lastInterval > period:
			function( argument )
			self.lastInterval = self.time.time()
	
	
	def mainloop(self, gamestate):
		inDeltas = []
		for bundle in self.recvBundles():
			packet, addr = bundle
			if packet: print('packet: '+packet)
			
			if packet[0] == self.netcom.codes['net']:
				self.handleNetBundle(bundle)
			
			if packet[0] == self.netcom.codes['throw']:
				seq, data = self.netcom.clientParseThrowPacket(packet)
				if data and seq > self.lastThrowSeq:
					self.lastThrowSeq = seq
					print("throw in: "+data)
					inDeltas.append(data)
			
			if packet[0] == self.netcom.codes['stream']:
				pass
		
		if not self.connected:
			if self.time.time()-self.lastConnectionAttempt > self.connectionAttemptPeriod:
				print("attempting handshake...")
				request = self.netcom.codes['net'] + b'c' + bytes(self.username)
				self.sock.sendto(request, self.addr)
				self.lastConnectionAttempt = self.time.time()
				self.connectionAttempts+=1
		
		return inDeltas



Client = initializeClient( ('192.168.1.101', 3203), "Jimmy" )
print("Client initiated and running.")
import time
lastThrow = 0.0
while True:
	Client.mainloop(None)
	if Client.connected:
		if time.time()-lastThrow > 1.0:
			Client.throw("OLIOLIO!")
			lastThrow = time.time()

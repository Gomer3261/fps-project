Server=None # Server Object.
Client=None # Client Object.
inBuffer=[] # List of messages that Network has recieved.




class initiateServer:
	def __init__(self,port):
		import socket
		self.buf=1024
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(('',port))
		
		connections = {} # Dictionary of connections

	class makeConnection:
		def __init__(self,addr,username):
			self.addr=addr
			self.username=username
			self.lastThrowInSeq = 0
			self.nextThrowOutSeq = 0
		def getThrowOutSeq(self): s=self.nextThrowOutSeq; self.nextThrowOutSeq+=1; return s
	
	def lowLevelStuff(self):
		import netfuncs
		data,addr = self.sock.recvfrom(self.buf)
		if data:
			if data[0]=="\x11": # It's a network packet.
				if data[1] == "c": # they want to initiate a connection.
					username=data[2:]
					self.connections[addr] = self.makeConnection(addr,username)
					packet = netfuncs.makeNetPacket('a')
					self.sock.sendto(packet,addr)
					
			if data[0]=="\x12": # It's an unreliable throw packet.
				seq = data[:11][1:]
				seqInt = int(seq)
				if not (seqInt <= self.connections[addr].lastThrowInSeq):
					# The packet is new.
					# what do I do with it!?
					
			if data[0]=="\x13": # It's a reliable send packet.
				pass




class initiateClient:
	def __init__(self,addr,username):
		self.addr=addr
		import socket
		self.buf=1024
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
		import time as self.time
		self.lastConnectionAttempt = 0.0
		self.connectionAttemptPeriod = 0.5 # will attempt every 0.5 seconds.
		self.connectionAttempts=0
		self.connected=False
	
	def attemptConnection(self):
		import netfuncs
		packet = netfuncs.makeNetPacket('c')
		self.sock.sendto(packet, self.addr)
		
		self.lastConnectionAttempt = self.time.time()
		self.connectionAttempts+=1
	
	def lowLevelStuff(self):
		if not self.connected:
			if self.time.time() - self.lastConnectionAttempt > 0.5:
				self.attemptConnection()
		
		data,addr = self.sock.recvfrom(self.buf)
		if data:
			if data[0]=="\x11": # It's a network packet.
				pass
					
			if data[0]=="\x12": # It's an unreliable throw packet.
				seq = data[:11][1:]
				seqInt = int(seq)
				if not (seqInt <= self.connections[addr].lastThrowInSeq):
					# The packet is new.
					# what do I do with it!?
					
			
			if data[0]=="\x13": # It's a reliable send packet.
				pass







def addToInBuffer(messages):
	global inBuffer
	for message in messages:
		inBuffer.append(message)
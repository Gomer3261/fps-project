class baseThrowHandler:
	def __init__(self, connection, sock):
		self.connection = connection
		self.sock = sock
		import pickle; self.pickle = pickle
		self.maxPayloadSize = 450
		self.initialize()
	
	# Functions to be replaced by server/client specific subclasses.
	def initialize(self):
		pass
	def getSeq(self):
		pass
	def getId(self):
		pass
	def chainSubmit(self, seq, partLabel, id, payload): # Submits packet to the series tracking system
		pass
	
	
	
	
	def throw(self, object): # Throw function used by server and client alike.
		payload = self.pickle.dumps(object)
		seq = self.getSeq()
		id = self.getId()
		
		# This breaks large packets into series packets.
		if len(payload) > self.maxPayloadSize:
			payloads = self.chunkifyData( payload, self.maxPayloadSize )
			i=1
			for payload in payloads:
				partLabel=(i,len(payloads))
				packet = self.pickle.dumps( (1,seq,partLabel,id,payload) )
				self.sock.sendto( packet, addr )
				i+=1
		# This sends out simple packets.
		else:
			packet = self.pickle.dumps( (1,seq,None,id,payload) )
			self.sock.sendto( packet, addr )
	
	
	
	
	def recv(self, packet):
		flag, seq, partLabel, id, payload = self.pickle.loads(packet)
		
		if partLabel: # This packet is part of a chain...
			self.chainSubmit(seq, partLabel, id, payload) # Submits chain packets to the chain tracking system
			object, id = self.chainExtract() # Potentially returns a chain that this packet completed.
		else:
			object = self.pickle.loads(payload)
		
		self.chainTimeoutLoop() # Kills any old chains
		return object, id
			
			
		
	
	def chunkifyData(self, data, max):
		chunks = []; newChunk = b''; count=0
		for byte in data:
			newChunk+=byte; count+=1
			if len(newChunk) == max: chunks.append(newChunk); newChunk=b''
		if newChunk: chunks.append(newChunk)
		return chunks










"""
import pickle

maxPayloadSize = 450

def pack(header, payload):
	return pickle.dumps(header) + b'\x11' +

def unpack(packet):
	return pickle.loads( packet )

def prepareThrow(payload, seq, id=None):
	packets = []
	payloadSize = len( pickle.dumps(payload) )
	if payloadSize <= maxPayloadSize:
		packets.append( pack( ) )
"""
import pickle
def pack(payload): return pickle.dumps(payload)
def unpack(packet): return pickle.loads(packet)

class createConnection:
	def __init__(self, parent, addr, id=None, username=None):
		self.parent=parent
		self.addr=addr
		self.id=id
		self.username=username
		import engine; self.engine=engine
		import pickle; self.pickle=pickle
		import time; self.time=time
		self.lastThrowSeq = 0 # for incoming
		self.nextThrowSeq = 1 # for outgoing
		self.lastContact = self.time.time()
	
	def contact(self): # function called when remote end contacts, to prevent timeout.
		self.lastContact = self.time.time()
	
	def hasTimedOut(self):
		if self.time.time()-self.lastContact > self.parent.timeout:
			return True # We've timed out.
		else: return False
	
	
	def throw(self, item):
		seq = self.nextThrowSeq; self.nextThrowSeq+=1
		payload = self.pickle.dumps(item)
		packet = self.pickle.dumps( (1,seq,None,self.engine.id,payload) )
		self.parent.sock.sendto( packet, self.addr )
	
	
	
	
	def handleThrowPacket(self, seq, label, id, payload):		
		if label: # This packet is part of a chain...
			self.chainSubmit(seq, label, id, payload) # Submits chain packets to the chain tracking system
			item = self.chainExtract() # Potentially returns a chain that this packet completed.
		else:
			item = self.pickle.loads(payload)
		#self.chainTimeoutLoop() # Kills any old chains
		return item
	
	def chunkifyData(self, data, max):
		chunks = []; newChunk = b''; count=0
		for byte in data:
			newChunk+=byte; count+=1
			if len(newChunk) == max: chunks.append(newChunk); newChunk=b''
		if newChunk: chunks.append(newChunk)
		return chunks
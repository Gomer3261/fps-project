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
		self.chainSystem = self.createChainSystem() # Keeps track of packet chains. Allows us to break packets up into smaller chunks.
		
		self.maxPayload=450 # in number of bytes.
	
	def contact(self): # function called when remote end contacts, to prevent timeout.
		self.lastContact = self.time.time()
	def hasGoneStale(self):
		if self.time.time()-self.lastContact > self.parent.timeout:
			return True # We've timed out.
		else: return False
	
			
	
	def throw(self, item):
		seq = self.nextThrowSeq; self.nextThrowSeq+=1
		payload = self.pickle.dumps(item)
		if len(payload) > self.maxPayload:
			payloads = self.chunkifyData(payload, self.maxPayload)
			expectedLinks = len(payloads)
			linkNumber=1
			for payload in payloads:
				packet = self.pickle.dumps( (1,seq,(linkNumber,expectedLinks),self.engine.id,payload) )
				self.parent.sock.sendto( packet, self.addr )
				linkNumber+=1
		else:
			packet = self.pickle.dumps( (1,seq,None,self.engine.id,payload) )
			self.parent.sock.sendto( packet, self.addr )
	
	
	
	def handleThrowPacket(self, seq, label, id, payload):
		"""
		One might think, that in theory, this method should only ever return a max of 1
		item at a time, and that's probably true but... whatever.
		"""
		items = []
		if label: # This packet is part of a chain...
			self.chainSystem.submit(seq, label, id, payload) # Submits chain packets to the chain tracking system
			payloads = self.chainSystem.extract() # Potentially extracts completed payloads.
			self.chainSystem.staleLoop() # Kills chains that have gone stale.
			for payload in payloads: items.append( self.pickle.loads(payload) )
		else:
			items = [ self.pickle.loads(payload) ]
		return items
	
	def chunkifyData(self, data, max):
		chunks = []; newChunk=bytearray(); count=0
		for byte in data:
			newChunk.append(byte); count+=1
			if len(newChunk) == max: chunks.append(newChunk); newChunk=bytearray()
		if newChunk: chunks.append(newChunk)
		return chunks
	
	
	
	
	
	class createChainSystem:
		"""
		The Chain System stores packets that are part of a series (I metaphorically call them chains,
		and the individual packets that make up a series are called links).
		When a packet is too large (over 450 bytes or whatever), we break it into a chain of links (packets)
		that are under 450 bytes. The chain system is responsible for collecting these links and rebuilding
		chains. If a chain exists for more than half a second, it's trashed.
		"""
		def __init__(self):
			self.chains = {}
		class createChain:
			def __init__(self, seq, expectedLinks, id):
				self.seq=seq; self.expectedLinks=expectedLinks; self.id=id
				self.links={}
				import time; self.time=time
				self.lastContact=self.time.time(); self.timeout=0.5
			def addLink(self, linkNumber, payload):
				self.links[linkNumber]=payload; self.lastContact = self.time.time()
			def extract(self):
				if len(self.links) == self.expectedLinks:
					totalPayload = b''
					for linkNumber in self.links: totalPayload+=self.links[linkNumber]
					return totalPayload
				else: return None
			def hasGoneStale(self):
				return (self.time.time()-self.lastContact > self.timeout)
		def submit(self, seq, label, id, payload):
			if not (seq in self.chains): # make new chain
				linkNumber, expectedLinks = label
				self.chains[seq]=self.createChain(seq, expectedLinks, id); self.chains[seq].addLink(linkNumber, payload)
			else: # add to existing chain
				self.chains[seq].addLink(linkNumber, payload)
		def extract(self):
			payloads = []
			for seq in self.chains:
				newPayload = self.chains[seq].extract()
				if newPayload: payloads.append(newPayload)
			return payloads
		def staleLoop(self):
			toRemove=[]
			for seq in self.chains:
				if self.chains[seq].hasGoneStale(): toRemove.append(seq)
			for seq in toRemove:
				del self.chains[seq]



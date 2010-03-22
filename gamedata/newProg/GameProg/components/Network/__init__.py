### Networking Component ###

class Class:
	"""
	Network Terminology:
	item = (flag, data) a basic piece of python information, used for all communications.
	ticket = an unique identification number for every TCP connection session.
	parcel = (ticket, item)
	addr = a UDP address data thingy.
	basket = (parcel, addr)
	bundle = (UID, item)
	"""
	import comms
	import classes
	import core
	
	def __init__(self, slab):
		self.slab = slab
		# A bundle is a pair, (UID, item)
		self.inBundles = []
		self.sendOutBuffer = []
		self.throwOutBuffer = []
		
		import socket
		self.IP = socket.gethostbyname(socket.gethostname())
		
		self.GPS = None # GamePlay Server
		self.GPC = None # GamePlay Client
		
		print("Networking's ready.")
	
	
	
	def run(self, Admin, GameState, Interface):
		"""
		Maintains GPS and GPC by running them. If they exist, that is.
		"""
		try:
			if self.GPS:
				parcels = self.GPS.run(Admin, GameState, Interface)
				bundles = self.convertParcelsToBundles(parcels)
				for bundle in bundles: self.inBundles.append(bundle)
				if not self.GPS.active: self.GPS = None; Interface.out("Gameplay server terminated peacefully.", console=True)
			
			if self.GPC:
				bundles = self.GPC.run(Admin, Interface)
				for bundle in bundles: self.inBundles.append(bundle)
				if not self.GPC.active:
					self.GPC = None
					Interface.out("Gameplay client terminated.")
					# We might have to restart the entire game by reinitializing via Admin at this point.
		except:
			import traceback; traceback.print_exc()
	
	def convertParcelsToBundles(self, parcels):
		bundles = []
		for parcel in parcels:
			try:
				ticket, item = parcel
				UID = self.GPS.getUIDByTicket(ticket)
				bundle = (UID, item); bundles.append(bundle)
			except: pass
		return bundles
	
	
	def startServer(self, address, Interface):
		"""
		Starts the GPS.
		"""
		self.GPS = self.core.GPS(address)
		bound = self.GPS.bind()
		if bound:
			Interface.out("Server successfully bound to %s"%address, note=True, console=True)
			Interface.out("If you're NOT behind a router, people over the internet can now connect to you at %s. If you are behind a router, people can connect to you at that address, but only over LAN."%address, note=False, console=False)
		else:
			Interface.out("Server failed to bind to %s"%address, note=True, console=True)
	
	def endServer(self):
		self.slab.Interface.out("Please be prepared to wait for up to 15 seconds for the gameplay server to terminate peacefully.")
		self.GPS.startShutdown()
	
	def startClient(self, address):
		"""
		Starts the GPC.
		"""
		self.GPC = self.core.GPC(address)
		self.GPC.initiateConnection()
	
	def outgoing(self, Admin, GameState):
		"""
		Sends/throws all of the items in the out buffers to the Host.
		If we are the host, then we just plop them straight into inBundles.
		If we're not the host, then we send them through the GPC (GamePlayClient).
		"""
		weAreHost = False
		if Admin.UID == GameState.getHost():
			weAreHost = True
		
		if weAreHost:
			# We just have to turn each item in the outgoing buffers, convert them into bundles
			# and then plop them right into the in buffer. Then clear the outgoing buffers.
			for item in self.sendOutBuffer:
				bundle = (Admin.UID, item)
				self.inBundles.append(bundle)
			for item in self.throwOutBuffer:
				bundle = (Admin.UID, item)
				self.inBundles.append(bundle)
			self.sendOutBuffer = []
			self.throwOutBuffer = []
		
		else:
			# We have to send/throw our crap through the GPC.
			pass
	
	def send(self, item):
		"""
		Puts an item in the outgoing buffer.
		"""
		self.sendOutBuffer.append(item)
	
	def throw(self, item):
		"""
		Puts an item in the outgoing buffer.
		"""
		self.throwOutBuffer.append(item)
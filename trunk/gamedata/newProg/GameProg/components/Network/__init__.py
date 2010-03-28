### Network Component ###

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
		
		self.gameStateFullDistroClock = self.comms.TIMER()
		self.gameStateShoutDistroClock = self.comms.TIMER()
		
		print("Networking's ready.")
	
	def sendText(self, UID, text):
		self.send( ('TXT', (UID, text)) )
	
	def getUserNameByTicket(self, ticket):
		username = "-NameError-"
		if self.GPS:
			UID = self.GPS.getUIDByTicket(ticket)
			if UID:
				username = self.slab.GameState.getUserName(UID)
		return username
	
	
	def gameStateDistro(self, GameState):
		"""
		If we're running a server, then we will distribute the GameState (full, and in changes) to each client.
		"""
		if self.GPS:
			if self.gameStateFullDistroClock.get() > 0.5:
				self.GPS.sendToAll( ('GS', ('FD', GameState.contents)) )
				self.gameStateFullDistroClock.reset()
			#if self.gameStateShoutDistroClock.get() > 0.1:
			if GameState.RequestHandler.shouts:
				self.GPS.sendToAll( ('GS', ('SD', GameState.RequestHandler.shouts)) )
				GameState.RequestHandler.shouts = [] # We have to clear the shouts here
			#self.gameStateShoutDistroClock.reset()
	
	
	
	def removeGameStateUsersWithNoConnection(self, GameState, Admin):
		toRemove = []
		for UID in GameState.contents['U']:
			noConnection = False
			userData = GameState.contents['U'][UID]
			ticket = userData['T']
			if self.GPS:
				session = self.GPS.tcpServer.getSession(ticket)
				if session:
					if not session.clientSock:
						noConnection = True
				else:
					noConnection = True
			else:
				noConnection = True
			if noConnection:
				if UID != Admin.UID:
					toRemove.append(UID)
		for UID in toRemove:
			GameState.removeUser(UID)
					
	
	
	def run(self, Admin, GameState, Interface):
		"""
		Maintains GPS and GPC by running them. If they exist, that is.
		"""
		try:
			if Admin.weAreHost():
				self.removeGameStateUsersWithNoConnection(GameState, Admin)
			
			if self.GPS:
				self.gameStateDistro(GameState)
				parcels = self.GPS.run(Admin, GameState, Interface, self)
				bundles = self.convertParcelsToBundles(parcels)
				for bundle in bundles: self.inBundles.append(bundle)#; print('GPS Bundle:', bundle)
				if not self.GPS.active: self.GPS = None; Interface.out("Gameplay server terminated peacefully.", console=True)
			
			if self.GPC:
				bundles = self.GPC.run(Admin, Interface)
				for bundle in bundles: self.inBundles.append(bundle)#; print('GPC Bundle:', bundle)
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
			except: import traceback; traceback.print_exc()
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
	
	def outgoing(self, Admin, GameState, Interface):
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
		else:
			if self.GPC:
				for item in self.sendOutBuffer:
					self.GPC.send(item)
					#print("GPC SENT:", item)
				for item in self.throwOutBuffer:
					self.GPC.throw(item)
					#print("GPC THREW:", item)
			else:
				Interface.out("Error: We're not the host, but there is no GPC?")
		self.sendOutBuffer = []
		self.throwOutBuffer = []
	
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
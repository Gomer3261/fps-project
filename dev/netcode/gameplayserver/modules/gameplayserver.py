#####################
### SERVER MODULE ###
#####################

class SERVER:
	LIFE = 1
	TERMINATE = 0
	
	info = {}
	info["details"] = {}
	info["stats"] = {}
	info["stats"]["clnum"] = 0
	
	connected = 0

	import handlers
	SERVER = handlers.SERVER # For hosting a server socket.
	CLIENT = handlers.CLIENT # For connecting as a client to the master server.
	CLIENTHANDLER = handlers.CLIENTHANDLER # For each connected gameplay client.

	### DEPRECATED
	#import serverclasses
	#SOCKET = serverclasses.SOCKET
	#MASTERSERVER = serverclasses.MASTERSERVER
	#CLIENT = serverclasses.CLIENT

	import theater
	clientTheater = theater.THEATER()

	import gamestate
	gamestate = gamestate.GAMESTATE()






	### Just a nifty little timer class, for timing the sending of gamestate information ###
	
	class TIMER():
		import time
		last = 0.0
		def __init__(self):
			self.reset()

		def reset(self):
			self.last = self.time.time()

		def get(self):
			dif = self.time.time() - self.last
			return dif
		
		def do(self, interval=1.0):
			# This is useful for an interval timer.
			# If you want something to happen every
			# interval seconds, call this function
			# and if it returns 1, then do it.
			# In other words, this returns 1 after
			# the given interval time has elapsed since
			# 1 was last returned. Get it?
			dif = self.get()
			if dif > interval:
				self.reset()
				return 1 # Do
			else:
				return 0 # Don't.

	checkupTimer = TIMER()
	fulldistroTimer = TIMER()
	shoutTimer = TIMER()




	


	##########################################
	###### ---------------------------- ######
	###### ------ GAMEPLAYSERVER ------ ######
	###### ---------------------------- ######
	##########################################

	def setDetails(self, details):
		self.info["details"] = details

	def refreshDetails(self):
		import detailreader
		details = detailreader.getDetails()
		if details:
			self.info["details"] = details

	def refreshStats(self):
		clnum = len(self.clientTheater.seats)

		self.info["stats"]["clnum"] = clnum

	def getFreshInfo(self):
		self.refreshDetails()
		self.refreshStats()
		return self.info

	# This is what effectively starts the server.
	def connect(self, mshost="chase.kicks-ass.net", msport=2340, TCP_port=2342, UDP_port=2343):
		import traceback
		
		self.sock = self.handlers.SERVER()
		self.msclient = self.CLIENT()

		try:
			self.sock.bind(TCP_port, UDP_port) # Binding the server socket
			if self.sock.bound:
				self.connected = 1
				print "Server has been successfully bound."
		except:
			print "There was an error binding the server:"
			traceback.print_exc()

		

		self.msclient.connect(mshost, msport) # Connecting to the master server

		if not self.msclient.connected:
			print "Failed to connect to Master Server. Players will only be able to find this server by manually joining your IP address."
		else:
			print "Connection to Master Server succeeded."

	def terminate(self):
		self.sock.terminate()
		print "	   Server Socket Terminated."
		self.msclient.terminate()
		print "	   Master Server Client Terminated."
		self.clientTheater.terminate()
		print "	   clientTheater and all of it's handlers Terminated."
		
		self.connected = 0
		self.LIFE = 0
		print "This Gameplay Server has been Terminated."







	### ======================================================================== ========================================================================
	### ======================================================================== ========================================================================
	### ======================================================================== ========================================================================
	
	def doNetworking(self):
		self.acceptClients()
		self.catchDistro()
		self.cleanUp()

	### ========================================================================

	def acceptClients(self):
		connection = self.sock.accept()
		if connection:
			# Creating client object
			handler = self.CLIENTHANDLER(connection, self.sock, 5.0)
			ticket = self.clientTheater.seatHandler(handler) # This puts the handler in a seat and gives us a ticket
			seat = self.clientTheater.seats[ticket]
			seat.info["loggedIn"] = ""
			print ">>> New Client Connection (%s); There are now %s clients" % (handler.ip, len(self.clientTheater.seats))

	def catchDistro(self):
		# Incoming UDP stuff for all clients appears on one socket; there is not one UDP socket for each client
		# (because UDP is a connectionless protocol). This method gets a packet, figures out to whom it belongs,
		# and then distributes it to them. Later on, they will check for it. Sound strange? Well too bad.
		stuff = self.sock.catch()

		if not stuff:
			return None

		ticket, flag, data, addr = stuff
		
		seat = self.clientTheater.getSeat(ticket)

		if not seat:
			print "		   Non-critical error: Client sent over UDP before they had a seat :D"
			return None
		
		client = seat.handler

		if not client:
			print "		   Lost UDP Packet, looking for %s" % (ticket)
			return None
		
		if not client.UDP_addr:
			print "		   UDP_addr set for seat %s." % (ticket)
			client.UDP_addr = addr

		# This distributes the UDP catch to the client it belongs to.
		client.distroCatch(flag, data)
		

	def cleanUp(self):
		self.clientTheater.cleanUp()
		if self.TERMINATE:
			print "\nTermination Sequence:"
			self.terminate()








	

	### ======================================================================== ========================================================================
	### ======================================================================== ========================================================================
	### ======================================================================== ========================================================================

	def interact(self):
		self.interactWithClientsA()
		self.interactWithClientsB()
		self.interactWithMasterServer()

	### ========================================================================
	def textEverybody(self, senderTicket, senderName, message):
		theater = self.clientTheater
		
		for ticket in theater.seats:
			seat = theater.seats[ticket]
			client = seat.handler

			if client:
				callsign = "(%s/%s)" % (client.ip, ticket)
				d = {}
				d["T"] = senderTicket
				d["N"] = senderName
				d["M"] = message
				
				client.send("TXT", d)




	def interactWithClientsA(self):
		### ========================================================================
		### Actions based on information received from clients
		### ========================================================================
		theater = self.clientTheater
		#import comms
		
		for ticket in theater.seats:
			seat = theater.seats[ticket]
			client = seat.handler

			if client:
				callsign = "(%s;%s)" % (client.ip, ticket)
				client.sendloop()
				
				items = client.getItems()
				for item in items:
					# There is an item from this ticket.
					seat.contact() # So we can keep the seat active.
					flag, data = item[0], item[1]
					#print "		Client %s sent a '%s' package." % (callsign, flag)

					### ------------------------------------------------------------------------
					### High Priority Operations (Should be entirely TCP)
					### ------------------------------------------------------------------------

					if flag.lower() == "ticket":
						print "		   %s requested their ticket." % (callsign)
						f = "ticket"
						d = ticket
						client.send(f, d)

					if flag.lower() == "query":
						print "		   %s query'd." % (callsign)
						f = "info"
						d = self.getFreshInfo()
						client.send(f, d)

					if flag.lower() == "bye":
						print "		   %s is saying 'bye'. Terminating their connection..." % (callsign)
						seat.terminate() # Terminating the entire seat, not just the handler.

					if flag.lower() == "terminateserver":
						print "		   %s is telling the server to terminate." % (callsign)
						self.textEverybody(0, "Server", "%s has ordered the server to terminate."%(self.gamestate.getPlayerName(ticket)))
						self.TERMINATE = 1
					
					if flag.lower() == "join":
						username = data
						if not username:
							username = "-NameError-"
						print "		   %s wants to join the game as '%s'." % (callsign, username)
						
						if (not self.gamestate.userIsInGame(ticket)) and (not self.gamestate.userNameIsInGame(username)):
							self.gamestate.addUser(ticket, username)
							client.send("join", 1)
							print "	   %s successfully joined the game as '%s'." % (callsign, username)
							self.textEverybody(0, "Server", "%s has joined the game."%(username))
						else:
							client.send("join", 0)
							print "		   Join operation failed for %s." % (callsign)
							self.textEverybody(0, "Server", "%s tried to join the game but failed (Name collision?)"%(username))
							

					if flag.lower() == "txt":
						message = data
						username = self.gamestate.getUserName(ticket)
						print "TXT: %s: %s" % (username, message)
						self.textEverybody(ticket, username, message)

					if flag.lower() == "hi":
						print "Got Hi!"

					### ------------------------------------------------------------------------
					### Gameplay Priority Operations (Usually UDP)
					### ------------------------------------------------------------------------

##					  if flag.lower() == "upc": # updatePlayerCustom
##						  A = data[0]
##						  D = data[1]
##						  self.gamestate.upc(ticket, A, D)
##						  #print "GameState Updated:\n\n%s\n\n\n"%(self.gamestate.contents)
##
##					  if flag.lower() == "upa": # updatePlayerAttributes
##						  A = data
##						  self.gamestate.upa(ticket, A)
##						  #print "GameState Updated:\n\n%s\n\n\n"%(self.gamestate.contents)
##
##					  if flag.lower() == "ar":
##						  request = data[0]
##						  d = data[1]
##						  self.gamestate.ar(ticket, request, d)
##						  if request == "suicide":
##							  self.textEverybody(0, "Server", "%s manually commited suicide."%(self.gamestate.getPlayerName(ticket)))
##							  self.textEverybody(0, self.gamestate.getPlayerName(ticket), "IMMA RETARD!")
##						  #print "-Action Request: %s" % request
					
					# All gamestate changes should now be in GameStateChanges form ("gsc").
					if flag.lower() == "gsc":
						changes = data
						self.gamestate.applyChanges(changes)

	

	def interactWithClientsB(self):
		### ========================================================================
		### Actions not based on information recieved.
		### ========================================================================
		theater = self.clientTheater

		### Checkup Distro ###
		checkupTime = self.checkupTimer.do(0.5)
		if checkupTime:

			for ticket in theater.seats:
				seat = theater.seats[ticket]
				client = seat.handler

				if client:
					callsign = "(%s/%s)" % (client.ip, ticket)

					client.throw("CH", 1)
		
		### Full Distro ###
		fulldistrotime = self.fulldistroTimer.do(5.0)
		if fulldistrotime:

			for ticket in theater.seats:
				seat = theater.seats[ticket]
				client = seat.handler

				if client:
					callsign = "(%s/%s)" % (client.ip, ticket)

					client.throw("FD", self.gamestate.contents)

		### Shout Distro ###
		shouttime = self.shoutTimer.do(0.05)
		if shouttime:
			changes = self.gamestate.getChanges()
			if changes:
				for ticket in theater.seats:
					seat = theater.seats[ticket]
					client = seat.handler

					if client:
						callsign = "(%s/%s)" % (client.ip, ticket)
						client.throw("SH", changes)
						#print "CHANGES:", changes

	

	def interactWithMasterServer(self):
		import comms

		if self.msclient.connected:
			# Do send loop (sends overflowed data)
			self.msclient.sendloop()
			
			# Get packages
			packages = self.msclient.recv()

			for package in packages:
				flag, data = comms.unpack(package)
				print "	   MasterServer sent a '%s' package." % (flag)

				if flag.lower() == "query":
					f = "info"
					d = self.getFreshInfo()
					self.msclient.send(f, d)










	### ======================================================================== ========================================================================
	### ======================================================================== ========================================================================
	### ======================================================================== ========================================================================

	def play(self):
		self.cleanGamestate()

	### ========================================================================
	
	def cleanCategory(self, category="U"):
		gamestate = self.gamestate
		theater = self.clientTheater
		
		ticketsToRemove = []
		
		for ticket in gamestate.contents[category]:
			if not theater.hasSeat(ticket):
				ticketsToRemove.append(ticket)
		
		for ticketToRemove in ticketsToRemove:
			if category == "U":
				self.textEverybody(0, "Server", "%s has left the game."%(gamestate.contents[category][ticketToRemove]["N"]))
			del gamestate.contents[category][ticketToRemove]
			print "	   %s removed from gamestate (%s)." % (ticket, category)

	def cleanGamestate(self):
		# This method deletes players from the gamestate
		# when their connection goes away.
		
		gamestate = self.gamestate
		theater = self.clientTheater
		
		categories = ["U", "P"]
		for category in categories:
			self.cleanCategory(category)



server = SERVER()

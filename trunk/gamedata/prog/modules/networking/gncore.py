# gncore: for communication with gameplay servers

gnclient = None
basicUpdateTimer = None
checkTimer = None
expiration = 10.0

def connect(name="-NameError-", host="stokes.dyndns.org"):
	global gnclient, GNCLIENT
	
	import modules
	terminal = modules.interface.terminal
	info = modules.gamecontrol.info
	
	gnclient = GNCLIENT(expiration)
	
	TCPport = 2342
	UDPport = 2343
	
	terminal.output('Attempting connection with "%s"'%(host))
	
	gnclient.connect(host, TCPport, UDPport)
	
	if gnclient.connected:
		terminal.output("Connection success!")
		gnclient.requestTicket()
		gnclient.joinGame(name)
		info.set("online")
	else:
		terminal.output("Error: Connection to gameplay server failed.")
		info.set("offline")

def text(message):
	global gnclient
	if gnclient:
		if gnclient.connected:
			gnclient.send("txt", message)
			return None
	import modules
	terminal = modules.interface.terminal
	terminal.output("You have to be connected to text message.")
		
		

def run(con):
	# Runs the networking!
	global gnclient
	global basicUpdateTimer
	global checkTimer
	
	import modules
	
	### TIMERS ###
	if not basicUpdateTimer:
		basicUpdateTimer = modules.timetools.TIMER()
	if not checkTimer:
		checkTimer = modules.timetools.TIMER()
	
	gamecontrol = modules.gamecontrol
	info = gamecontrol.info
	gamestate = gamecontrol.gamestate.gamestate
	director = gamecontrol.director
	router = director.router
	localgame = gamecontrol.localgame
	
	terminal = modules.interface.terminal
	notes = modules.interface.notes
	
	networking = modules.networking
	
	if info.mode == "online":
		#print "ONLINE"
		# Okay, we need to get the communication going I suppose
		
		if gnclient.connected:
			#print "CONNECTED"
			# Woot! We're already connected!
			
			# Let's do a UDP checkup loop, eh?
			# This keeps the server aware that we are still connected and happy.
			# It also gives the server our UDP Identifications.
			timeToSendCheck = checkTimer.do(0.5) # Every half second
			if timeToSendCheck:
				gnclient.throw(gnclient.ticket, "CH", 1)
			
			
			
			# Okay, now we're going to do a sendloop, to help clear the sendbuffer.
			gnclient.sendloop()
			
			####################################################
			### ======------ INCOMING INFO LOOP ------====== ###
			####################################################
			# Okay, here's some real business!
			
			items = gnclient.getItems()
			for item in items:
				gnclient.contact() # We've got contact from the server, so we do this so we don't timeout.
				flag = item[0]
				data = item[1]
				
				
				### ======------ High Priority Information ------====== ###
				
				if flag.lower() == "ticket":
					# Yay, we've got our ticket!
					gnclient.ticket = data
					info.ticket = data
					terminal.output("Got ticket!: %s"%(info.ticket))
				
				if flag.lower() == "join":
					if data:
						info.inGame = 1 # WOOT!
						terminal.output("We're in the game! The online game! WOO!")
						localgame.players.killAllPlayers()
				
				if flag.lower() == "info":
					if data:
						terminal.output("Server Query Information:")
						for key in data["details"]:
							value = data["details"][key]
							terminal.output("%s: %s"%(key, value))
						for key in data["stats"]:
							value = data["stats"][key]
							terminal.output("%s: %s"%(key, value))
					else:
						terminal.output("There was some kind of problem querying the server.")
				
				if flag.lower() == "txt":
					senderTicket = data["T"]
					senderName = data["N"]
					senderMessage = data["M"]
					m = "%s: %s"%(senderName, senderMessage)
					terminal.output(m)
					if senderTicket != info.ticket:
						notes.notify(m)
				
				
				### ======------ Gamestate Operations ------====== ###
				
				if flag.lower() == "fd":
					# Full gamestate distribution
					#print "	   GOT FD"
					gamestate.applyFulldistro(data)
				
				if flag.lower() == "sh":
					#print "	   GOT SH"
					# Shout containing changes
					gamestate.applyChanges(data)
				
				if flag.lower() == "ch":
					pass
					#print "	   GOT CH"
			
			
			
			
			### TERMINATE IF STALE ###
			#print "CHECKING STALE"
			terminated = gnclient.terminateIfStale()
			if terminated:
				#print "WENTSTALE"
				info.set("offline")
				localgame.players.killAllPlayers()
				m = "Connection to the server went stale; you've been disconnected."
				terminal.output(m)
				notes.notify(m)

						
					




##########################################
### ======------ GNCLIENT ------====== ###
##########################################

import handlers
class GNCLIENT(handlers.CLIENT):
	
	ticket = None # You cannot send any data over UDP until you get your ticket.
	
	def requestTicket(self):
		self.send("ticket", "plz")

	def joinGame(self, name):
		self.send("join", name)
	
	def kissGoodbye(self):
		self.send("bye", 1)

gnclient = GNCLIENT(expiration)


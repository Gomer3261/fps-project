###################
###   GN_Main   ###
###################
### Communicates with a gameplay server

import GameLogic as gl
import Rasterizer

con = gl.getCurrentController()
own = con.owner

#sen = con.sensors["sen"]
#act = con.actuators["act"]

### ------------------------------------------------ ###
### Importing Modules
### ------------------------------------------------ ###
import modules

slab = modules.slab

mousetools = modules.gamesystems.mousetools
pathfinding = modules.gamesystems.pathfinding
damper = modules.gamesystems.damper
ballistics = modules.gamesystems.ballistics
player = modules.gamesystems.player

terminal = modules.systems.terminal
options = modules.systems.options
inputs = modules.systems.inputs
profiling = modules.systems.profiling
notifications = modules.systems.notifications

mscom = modules.networking.mscom
gncore = modules.networking.gncore

gamemod = modules.systems.gamemod

GUI = modules.GUI
### ------------------------------------------------ ###
gnclient = gncore.gnclient
gamestate = gamemod.gamestate
gamecontroller = gamemod.gamecontroller
###






def output(s):
	global terminal
	global notifications
	terminal.output(s)
	notifications.notify(s)



# If we are connected, then we've got to start the communication flow.
if gamecontroller.mode == "online":
	
	if gnclient.connected:
		
		# Let's do a UDP checkup loop eh?
		# This keeps the server aware that we are still connected and happy,
		# and it also gives the server our UDP Identifications.
		timeToSendCheck = gncore.checkTimer.do(0.5) # Every half second
		if timeToSendCheck:
			gnclient.throw(gnclient.ticket, "CH", 1)
			print "CH SENT"
		
		gnclient.sendloop()
		
		### Incoming Information Loop ###
		items = gnclient.getItems()
		for item in items:
			gnclient.contact()
			flag = item[0]
			data = item[1]
			
			### ========================================================================
			### === High Priority Operations
			### ========================================================================
			
			if flag.lower() == "ticket":
				gnclient.ticket = data
				gamecontroller.ticket = data
				m = "Got ticket: %s" % (gamecontroller.ticket)
				output(m)
			
			if flag.lower() == "join":
				if data:
					gamecontroller.inGame = 1
					m = "You've successfully joined the game!"
					output(m)
					player.killPlayer = 1
				else:
					gamecontroller.inGame = 0
					m = "Error: Something when wrong when you tried to join the game."
					output(m)
			
			if flag.lower() == "info":
				if data:
					output("Server Query Information:")
					for key in data["details"]:
						value = data["details"][key]
						m = "%s: %s" % (key, value)
						output(m)
					for key in data["stats"]:
						value = data["stats"][key]
						m = "%s: %s" % (key, value)
						output(m)
				else:
					output("There was some kind of problem with querying the server.")
			
			if flag.lower() == "txt":
				senderTicket = data["T"]
				senderName = data["N"]
				senderMessage = data["M"]
				m = "%s: %s" % (senderName, senderMessage)
				output(m)
			
			
			
			
			### ========================================================================
			### === Gamestate Operations
			### ========================================================================
			
			if flag.lower() == "fd":
				# Full Gamestate Distribution
				gamestate.applyFulldistro(data)
			
			if flag.lower() == "sh":
				# Shout containing changes
				changes = data
				gamestate.applyChanges(changes)
				#print "CHANGES APPLIED:\n%s\n\n\n"%(changes)
			
			if flag.lower() == "ch":
				print "GOT CH"
				
	
	
	
		### Terminate if stale ###
		terminated = gnclient.terminateIfStale()
		if terminated:
			gamecontroller.set("offline")
			output("Connection to gameplay server has been lost!")

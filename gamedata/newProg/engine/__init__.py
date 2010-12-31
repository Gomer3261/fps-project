import engine
import engine.gamestate as gamestateModule
import engine.network as network
import engine.entities as entities
import engine.interface

gamestate=None
entityController=None

host=0
net=1
id=None # We get our id from gamestate.addUser
username="LiamNeeson"

# defining mode
if host and net: mode="server"
if (not host) and net: mode="client"
if host and (not net): mode="local"
if (not host) and (not net): mode="replay"

INIT = False

### Globals above this line.

network.addr = "192.168.1.101"
network.port = 3201

def DEBUG(title):
	print("\n\nDEBUG: ", title)
	print("engine.id: ", engine.id)
	print("gamestate.data: ", gamestate.data)
	print("gamestate.delta: ", gamestate.delta)
	print("\n\n")

def initialize():
	global gamestateModule, network, entities, interface
	global gamestate, entityController
	global host, net, id, username, mode
	global INIT
	
	gamestate = gamestateModule.initializeGamestate()
	entityController = entities.initializeEntityController()
	interface = interface.initializeInterface()
	
	if host:
		engine.id = gamestate.addUser( username )
		gamestate.addEntity( 'director' )
		
	INIT = True
	
	print('='*50)
	print("GAME INITIALIZED")
	print("    mode: "+mode)
	print('='*50)

def mainloop():
	global gamestateModule, network, entities, interface
	global gamestate, entityController
	global host, net, id, username, mode
	global INIT
	
	if not INIT: initialize()
		
	# Server routines.
	if mode=="server" and not network.connection:
		network.connection = network.server.initializeServer( network.port ) # Server initiation.
	elif mode=="client" and not network.connection:
		network.connection = network.client.initializeClient( (network.addr,network.port), username ) # Client initiation.
	else:
		if net:
			if not host:
				if gamestate.delta and network.connection.isConnected(): network.connection.throw( gamestate.delta )
				gamestate.delta.clear()
			deltas = network.connection.mainloop( gamestate ) # network uses gamestate to sync user id's.
			for delta in deltas: gamestate.mergeDelta( delta )
			if host:
				if gamestate.delta and network.connection.isConnected(): network.connection.throwToAll( gamestate.delta )
				if network.connection.isConnected(): network.connection.interval( network.connection.throwToAll, gamestate.data, 2.0 )
		gamestate.applyDelta()
		gamestate.delta.clear()

	
	### UNIVERSAL ROUTINES
	# These apply to server, client, and local modes.
	entityController.conform( gamestate ) # replicator emulates the gamestate by adding objects or removing them based on what the gamestate says.
	
	for idloop in entityController.entities: # We loop through every entity.
		entity = entityController.entities[idloop]
		deltaDataList = entity.run( gamestate ) # Running controlled entities.
		for deltaData in deltaDataList:
			if deltaData: gamestate.mergeDelta(deltaData)
					
	#interface.runDisplays() #not available until proper bgui implementation
	#gamestate.clear() # just for giggles
	
	import bge
	keyboard = bge.logic.keyboard
	if keyboard.events[bge.events.DKEY] == 3:
		DEBUG("KEYPRESS")
		




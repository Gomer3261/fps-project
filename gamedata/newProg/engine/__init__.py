import engine
import engine.gamestate as gamestateModule
import engine.network
import engine.entities
import engine.interface
import engine.camera

gamestate=None
entityController=None

host=1
net=0
id=None # We get our id from gamestate.addUser
username="Jesus"

# defining mode
if host and net: mode="server"
if (not host) and net: mode="client"
if host and (not net): mode="local"
if (not host) and (not net): mode="replay"

INIT = False

### Globals above this line.

network.addr = "192.168.1.101"
network.port = 3202

# Debug function prints out important game info.
def DEBUG(title="unspecified"):
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

	
	### UNIVERSAL ROUTINES: These apply to server, client, and local modes.
	entityController.conform( gamestate ) # replicator emulates the gamestate by adding objects or removing them based on what the gamestate says.
	
	for idloop in entityController.entities: # We loop through every entity.
		entity = entityController.entities[idloop]
		deltaDataList = entity.run( gamestate ) # Running controlled entities.
		for deltaData in deltaDataList:
			if deltaData: gamestate.mergeDelta(deltaData)
					
	interface.main() #not available until proper bgui implementation
	
	engine.camera.resetPriority() # Clearing the priority so that the cameras next frame can compete with each other.
	
	# Debug on keypress of the asterisk * key on the numpad.
	import bge
	keyboard = bge.logic.keyboard
	if keyboard.events[bge.events.PADASTERKEY] == 3:
		DEBUG("KEYPRESS")





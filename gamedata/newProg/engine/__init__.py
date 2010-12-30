import engine
import engine.gamestate as gamestateModule
import engine.network as network
import engine.entities as entities
import engine.interface

gamestate=None
entityController=None

host=1
net=0
id=1

# defining mode
if host and net: mode="server"
if (not host) and net: mode="client"
if host and (not net): mode="local"
if (not host) and (not net): mode="replay"

INIT = False

### Globals above this line.

network.addr = "96.54.129.113"
network.port = 3205

def initialize():
	global gamestateModule, network, entities, interface
	global gamestate, entityController
	global host, net, id, mode
	global INIT
	
	gamestate = gamestateModule.initializeGamestate()
	entityController = entities.initializeEntityController()
	interface = interface.initializeInterface()
	
	gamestate.mergeDelta( {'E':{gamestate.getNextId():{'t':'cube','c':engine.id}}} )
	#self.data["E"][self.getNextId()] = {"c":engine.id, "t":"cube"}
	
	INIT = True
	
	print('='*50)
	print("GAME INITIALIZED")
	print("    mode: "+mode)
	print('='*50)

def mainloop():
	global gamestateModule, network, entities
	global gamestate, entityController, interface
	global host, net, id, mode
	global INIT
	
	if not INIT: initialize()
	
	# Server routines.
	if mode=="server" and not network.connection:
		network.connection = network.server.initializeServer( network.port ) # Server initiation.
	elif mode=="client" and not network.connection:
		network.connection = network.client.initializeClient( ('',network.port), "Cartman" ) # Client initiation.
	else:
		if net:
			if not host:
				network.connection.throw( gamestate.delta )
				gamestate.delta.clear()
			network.connection.mainloop( gamestate ) # network uses gamestate to sync user id's.
			for item in network.connection.inBuffer:
				gamestate.mergeDelta( item )
			if host:
				network.connection.throwToAll( gamestate.delta )
				network.connection.interval( network.connection.throwToAll, gamestate.data, 2.0 )
		gamestate.applyDelta()
		gamestate.delta.clear()

	
	### UNIVERSAL ROUTINES
	# These apply to server, client, and local modes.
	entityController.conform( gamestate ) # replicator emulates the gamestate by adding objects or removing them based on what the gamestate says.
	
	for id in entityController.entities: # We loop through every entity.
		entity = entityController.entities[id]
		deltaDataList = entity.run( gamestate ) # Running controlled entities.
		for deltaData in deltaDataList:
			if deltaData: gamestate.mergeDelta(deltaData)
		
	#interface.runDisplays() #not available until proper bgui implementation
	#gamestate.clear() # just for giggles
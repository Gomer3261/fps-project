import engine.gamestate as gamestateModule
import engine.network
import engine.entities

gamestate=None
entityController=None

INIT = False

def initialize(host=1, net=0):
	global gamestate, gamestateModule, network, entities, entityController, INIT
	gamestate = gamestateModule.initiateGamestate(host, net)
	entityController = entities.initiateEntityController()
	network.addr = "96.54.129.113"
	network.port = 3205
	INIT = True
	print('='*50)
	print("GAME INITIALIZED")
	print("    mode: "+gamestate.mode)
	print('='*50)

def mainloop():
	global gamestate, gamestateModule, network, entities, entityController, INIT
	if not INIT: initialize()
	
	# Server routines.
	if gamestate.mode=="server" and not network.connection:
		network.connection = network.server.initiateServer( network.port ) # Server initiation.
	elif gamestate.mode=="client" and not network.connection:
		network.connection = network.client.initiateClient( ('',network.port), "Cartman" ) # Client initiation.
	else:
		if gamestate.net:
			if not gamestate.host:
				network.connection.throw( gamestate.delta )
				gamestate.delta.clear()
			network.connection.mainloop( gamestate ) # network uses gamestate to sync user id's.
			for item in network.connection.inBuffer:
				gamestate.mergeDelta( item )
			if gamestate.host:
				network.connection.throwToAll( gamestate.delta )
				network.connection.interval( network.connection.throwToAll, gamestate.data, 2.0 )
		gamestate.applyDelta()
		gamestate.delta.clear()

	
	### UNIVERSAL ROUTINES
	# These apply to server, client, and local modes.
	
	entityController.conform( gamestate ) # replicator emulates the gamestate by adding objects or removing them based on what the gamestate says.
	
	for id in entityController.entities: # We loop through every entity.
		entity = entityController.entities[id]
		entity.conform( gamestate ) # Each entity conforms to the gamestate as it sees fit.
		if entity.getMode() == "control": # Only control entities send info to the gamestate (to request changes)
			deltaData, memos = entity.run( gamestate ) # Running controlled entities.
			if deltaData: gamestate.mergeDelta(deltaData)
			if memos: network.send(memos)
import engine.gamestate
import engine.network

gamestate = gamestate.initiateGamestate()

network.addr = "96.54.129.113"
network.port = 3205

def mainloop():
	
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
	
	replicator.conform( gamestate ) # replicator emulates the gamestate by adding objects or removing them based on what the gamestate says.
	
	for entity in replicator.entities: # We loop through every entity.
		entity.conform( gamestate ) # Each entity conforms to the gamestate as it sees fit.
		if entity.getMode() == "control": # Only control entities send info to the gamestate (to request changes)
			deltaData, memos = entity.run( gamestate ) # Running controlled entities.
			if deltaData: gamestate.mergeDelta(deltaData)
			if memos: network.send(memos)
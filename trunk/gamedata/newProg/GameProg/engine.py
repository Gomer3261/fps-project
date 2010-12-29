# Our Game Engine Within A Game Engine.

GameState.host=False # Designates if we are the host.
GameState.net=True # Designates if this will take place over internet/lan.

if GameState.host and GameState.net: GameState.mode="server"
if (not GameState.host) and GameState.net: GameState.mode="client"
if GameState.host and (not GameState.net): GameState.mode="local"
if (not GameState.host) and (not GameState.net): GameState.mode="replay"

Network.addr = "96.54.129.113"
Network.port = 3205



def MainLoop():
	
	# Server routines.
	if GameState.mode=="server" and not Network.Connection:
		Network.Connection = Network.initiateServer( Network.port ) # Server initiation.
	elif GameState.mode=="client" and not Network.Connection:
		Network.Connection = Network.initiateClient( ('',Network.port), "Cartman" ) # Client initiation.
		
	else:
		if GameState.mode="client":
			Network.Connection.throw( GameState.delta )
			GameState.delta.clear()
		Network.Connection.mainloop( GameState ) # Network uses gamestate to sync user id's.
		for item in Network.Connection.inBuffer:
			GameState.mergeDelta( item )
		if GameState.mode=="server": 
			Network.Connection.throwToAll( GameState.delta )
			Network.Connection.interval( Network.Connection.throwToAll, GameState.data, 2.0 )
		GameState.applyDelta()
		GameState.delta.clear()

	
	### UNIVERSAL ROUTINES
	# These apply to server, client, and local modes.
	
	LocalGame.conform( GameState ) # LocalGame emulates the GameState by adding objects or removing them based on what the GameState says.
	
	for entity in LocalGame.entities: # We loop through every entity.
		entity.conform( GameState ) # Each entity conforms to the GameState as it sees fit.
		if entity.getMode() == "control": # Only control entities send info to the gamestate (to request changes)
			deltaData, memos = entity.run( GameState ) # Running controlled entities.
			if deltaData: GameState.mergeDelta(deltaData)
			if memos: Network.send(memos)
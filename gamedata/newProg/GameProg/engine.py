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
	if GameState.mode == "server":
		if not Network.Server:
			Network.Server = Network.initiateServer(Network.port) # Server initiation.
		else:
			packets = Network.getIncoming()
			newUsers = Network.handleNetPackets(packets)
			GameState.deltaUsers( newUsers, departedUsers ) # Adds or removes users.
			GameState.interpret( Network.handleThrownPackets(packets) )
			GameState.interpret( Network.handleSentPackets(packets) )
			Network.send( GameState.data, 3.0 ) # Reliably sends out a full copy of the GameState.
			Network.throw( GameState.deltaData, 0.1 ) # Unreliably throws changes in the GameState to clients.
	
	# Client routines
	if GameState.mode == "client":
		if not Network.Client:
			Network.Client = Network.initiateClient( Network.addr,Network.port )
		else:
			packets = Network.getIncoming()
			if not Network.Client.connected: Network.Client.attemptConnection(packets)
			GameState.interpret( Network.handleThrownPackets(packets) )
			GameState.interpret( Network.handleSentPackets(packets) )
			Network.throw( GameState.deltaData, 0.1 ) # Unreliably throws requested GameState changes to the server.
	
	
	### UNIVERSAL ROUTINES
	# These apply to server, client, and local modes.
	
	LocalGame.conform( GameState ) # LocalGame emulates the GameState by adding objects or removing them based on what the GameState says.
	
	for entity in LocalGame.entities: # We loop through every entity.
		entity.conform( GameState ) # Each entity conforms to the GameState as it sees fit.
		if entity.getMode() == "control": # Only control entities send info to the gamestate (to request changes)
			deltaData, memos = entity.run() # Running controlled entities.
			if deltaData: GameState.mergeDelta(deltaData)
			if memos: Network.send(memos)
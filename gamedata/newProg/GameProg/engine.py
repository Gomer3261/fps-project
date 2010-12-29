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
	
	# Server exclusive routines.
	if GameState.mode == "server":
		if not Network.Server:
			Network.Server = Network.initiateServer(Network.port) # Server initiation.
		else:
			newUsers = Network.lowLevelStuff() # Asyncronously accepts new connections after giving them the GameState and UID.
			GameState.addUsers( newUsers ) # Adds any new users to the GameState.
			Network.send( GameState.data, 5.0 ) # Sends out a full gamestate package (sends are reliable UDP)
			Network.throw( GameState.deltaData, 0.1 ) # Throws (unreliably transfers over UDP) changes in the GameState to clients.
	
	# Client exclusive routines
	if GameState.mode == "client":
		if not Network.Client:
			Network.Client = Network.initiateClient( Network.addr,Network.port )
	
	if GameState.mode=="client" or GameState.mode=="server":
		messages = Network.catchMessages()
		if messages: Network.addToInBuffer(messages)
	
	### UNIVERSAL ROUTINES
	# These apply to server, client, and local modes.
	
	GameState.interpret( Network.inBuffer ) # The GameState interprets incoming messages.
	
	LocalGame.conform( GameState ) # LocalGame emulates the GameState by adding objects or removing them based on what the GameState says.
	
	for entity in LocalGame.entities: # We loop through every entity.
		entity.conform( GameState ) # Each entity conforms to the GameState as it sees fit.
		if entity.getMode() == "control": # Only control entities send info to the gamestate (to request changes)
			deltaData, memos = entity.run() # Running controlled entities.
			if deltaData: GameState.mergeDelta(deltaData)
			if memos: Network.send(memos)
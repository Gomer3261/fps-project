##########################################################
######## USER SETTING BOX OF FUN					######
##########################################################
host		= 1 # local:1, client:0, server:1			##
net			= 0 # local:0, client:1, server:1			##
username	= 'Gawd' # you'd better pick a cool name	##
ip			= 'chasemoskal.dyndns.org' # server host	##
port		= 3200 # the connection port				##
##########################################################




id=None
addr = (ip, port)
# defining mode
if host and net: mode="server"
if (not host) and net: mode="client"
if host and (not net): mode="local"
if (not host) and (not net): mode="replay"


###
import engine
import engine.gamestate as gamestateModule
import engine.network
import engine.entities
import engine.interface
import engine.camera
import engine.mouse
###

gamestate=None
entityController=None

# Master INIT
INIT = False




### Globals above this line ###





# Debug function prints out important game info.
def DEBUG(title="unspecified"):
	print("\n\nDEBUG: ", title)
	print("engine.id: ", engine.id)
	print("gamestate.data: ", gamestate.data)
	print("gamestate.delta: ", gamestate.delta)
	print("\n\n")

def initialize():
	global host, net, username, ip, port; global id, addr, mode
	global engine, gamestateModule, network, entities, interface, camera, mouse
	global gamestate, entityController; global INIT
	
	gamestate = gamestateModule.initializeGamestate()
	entityController = entities.createEntityController()
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
	global host, net, username, ip, port; global id, addr, mode
	global engine, gamestateModule, network, entities, interface, camera, mouse
	global gamestate, entityController; global INIT
	
	if not INIT: initialize()
	
	if mode=="server" and not network.remoteHandler:
		try: network.remoteHandler = network.createServer( addr ) # Server initiation.
		except: print("Network error: Address is already in use >:(")
	elif mode=="client" and not network.remoteHandler:
		network.remoteHandler = network.createClient( addr ) # Client initiation.
	else:
		if net:
			if not host:
				if gamestate.delta and network.remoteHandler.connection: network.remoteHandler.throw( ('d', gamestate.delta) )
				gamestate.delta.clear()
			items = network.remoteHandler.main( gamestate ) # network uses gamestate to sync user id's.
			for item in items:
				flag, stuff = item
				if flag=='d': gamestate.mergeDelta( stuff )
				elif flag=='f' and (not host): gamestate.data=stuff
				elif flag=='m': entityController.submitMemos(stuff)
				else: print("\nUnknown item type received:", item, "\n")
			if host:
				if gamestate.delta: network.remoteHandler.throwToAll( ('d',gamestate.delta) )
				if network.time.time()-network.lastGamestateDataSend > 2.0:
					network.remoteHandler.throwToAll( ('f',gamestate.data) )
					network.lastGamestateDataSend=network.time.time()
		gamestate.applyDelta()
		gamestate.delta.clear()

	
	### UNIVERSAL ROUTINES: These apply to server, client, and local modes.
	try: entityController.conform( gamestate ) # replicator emulates the gamestate by adding objects or removing them based on what the gamestate says.
	except: import traceback; traceback.print_exc()
	
	for idloop in entityController.entities: # We loop through every entity.
		try:
			entity = entityController.entities[idloop]
			deltaDataList, memoList = entity.run( gamestate ) # Running controlled entities.
			for deltaData in deltaDataList:
				if deltaData: gamestate.mergeDelta(deltaData)
			if memoList and (not host): network.remoteHandler.throw( ('m', memoList) )
		except: import traceback; traceback.print_exc()
	
	if host: # We remove entities with controller users that have left.
		toDelete=[]
		for idloop in entityController.entities:
			if not gamestate['E'][idloop]['c'] in gamestate['U']: toDelete.append(idloop)
		for idloop in toDelete: gamestate.removeEntity(idloop)
					
	interface.main() #not available until proper bgui implementation
	
	engine.camera.resetPriority() # Clearing the priority so that the cameras next frame can compete with each other.
	
	# Debug on keypress of the asterisk * key on the numpad.
	import bge
	keyboard = bge.logic.keyboard
	if keyboard.events[bge.events.PADASTERKEY] == 3:
		DEBUG("KEYPRESS")





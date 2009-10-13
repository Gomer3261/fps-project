# Just contains stuff for doing camera operations.
INIT = 0
ecam = None




import GameLogic
scene = GameLogic.getCurrentScene()

def init(con):
	global INIT
	global ecam
	ecam = con.actuators["ecam"].owner
	INIT = 1
	print "Camera Initiated"

def initLoop(con):
	global INIT

	if not INIT:
		init(con)






def reset():
	global scene
	global ecam
	#print "Resetting to", ecam
	scene.active_camera = ecam






def run(con):
	global scene
	global ecam
	
	initLoop(con)

	import modules
	localgame = modules.gamecontrol.localgame
	player = localgame.players.getLocalPlayer()
	explorer = localgame.explorers.explorer
	
	cam = ecam
	# Player Camera
	if player:
		if player.alive:
			cam = player.fpcam
			player.fpcam.lens = modules.interface.options.settings["lens"]
		elif explorer:
			if explorer.alive:
				cam = explorer.fpcam
				explorer.fpcam.lens = modules.interface.options.settings["lens"]
	elif explorer:
		if explorer.alive:
			cam = explorer.fpcam
			explorer.fpcam.lens = modules.interface.options.settings["lens"]
	
	scene.active_camera = cam

		

### THE CAMERA SYSTEM ###

# Okay, so this system is what handles which camera is active, and is partially responsible 
# for preventing blender crashing by deleting the active_camera game object.

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
	"""
	Resets the camera to the emergency camera.
	"""
	global scene
	global ecam
	scene.active_camera = ecam



def run(con):
	global scene
	global ecam
	
	# Asserts that we are initiated.
	initLoop(con)
	
	# Importing all of our modules and stuff.
	import modules
	localgame = modules.gamecontrol.localgame
	player = localgame.players.getLocalPlayer()
	explorer = localgame.explorers.explorer
	
	
	#### ================================================
	# Okay, so this is where we decide which camera becomes the active_camera.
	# First off, the new cam will always default to being the emergency cam.
	# That is, if no other cameras are available, we can always fall back on
	# the emergency camera (ecam).
	
	# What you see below, is a stack of if statements that may set the new cam.
	# As you'd discover, lower statements take priority. The Player's fpcam should
	# always be at the bottom of the stack, because the player's fpcam always takes
	# priority over all other cameras.
	#### ================================================
	
	
	# The camera defaults to being the ecam.
	cam = ecam
	
	
	
	# If there is an explorer entity out there, then we'll use that camera.
	if explorer:
		if explorer.alive:
			cam = explorer.fpcam
			explorer.fpcam.lens = modules.interface.options.settings["lens"]
	
	# If the player is alive, then we'll set the active cam to fpcam.
	if player:
		if player.alive:
			cam = player.fpcam
			player.fpcam.lens = modules.interface.options.settings["lens"]
	
	# Okay, now we actually assign the active_camera.
	scene.active_camera = cam






def followCamera(con):
	"""
	Just a quick little convenient function for getting an object to follow the active camera.
	Meant to be called from a module controller.
	"""
	global scene
	own = con.owner
	own.position = scene.active_camera.position



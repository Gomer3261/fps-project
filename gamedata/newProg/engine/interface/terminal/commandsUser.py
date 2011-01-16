import engine

helpText = """
Welcome to the FPS Project's in-game terminal.
All commands are executed as Python scripts.
Use listUserCommands() for a good time.
Precede your input with "/" to designate it as a python command or it will be sent as a text message.
"""

# ------------------------
# Terminal Commands
# ------------------------

def help(cmd = None):
	"""
	Usage: help(terminalCommand)
		Prints out text that should help you use the requested terminal command. If left blank, general help information is printed.
	"""
	if cmd:
		output(cmd.__doc)
	else:
		output(self.helpText)

def output(s):
	"""
	Usage: output(string)
		prints the given value in the terminal window.
	"""
	global engine
	s = str(s)
	engine.interface.output(s, 1, 0)

def clear():
	"""
	Usage: clear()
		Clears the terminal window of all text.
	"""
	global engine
	engine.interface.terminal.clear()

def listUserCommands():
	"""
	Usage: listUserCommands()
		Displays a list of commands available to the user.
	"""
	global engine
	for i in dir(engine.interface.terminal.commandsUser):
		# Filter out the python module stuff so we only get our commands
		if not i.startswith("__") and i != "helpText":
			output(i)
			
def setHistoryLimit(I):
	"""
	Usage: setHistoryLimit()
		Changes the number of items stored in the Terminal's history to the value given.
	"""
	global engine
	engine.interface.terminal.history.max = I






# ------------------------
# Informational Commands
# ------------------------

def gs():
	import engine
	output(engine.gamestate.data)
#	def ammo():
#		"""
#		Use this to see how much ammo you have.
#		"""
#		try:
#			import modules
#			localPlayer = modules.gamecontrol.localgame.players.getLocalPlayer()
#			ammopile = localPlayer.inventory.ammopile
#			output("Bullets in Ammopile:")
#			for bulletType in ammopile.bullets:
#				output("   %s: %s" % (bulletType, ammopile.bullets[bulletType]))
#			output("Bullets in Current Weapon:")
#			item = localPlayer.inventory.getActiveItem()
#			try:
#				c = 0
#				if item.firearm.chamber: c = 1
#				if item.firearm.magazine:
#					output("   %s (%s)"%(len(item.firearm.magazine)+c, item.firearm.bulletType))
#				else:
#					output("   None")
#			except:
#				import traceback
#				traceback.print_exc()
#		except:
#			output("Error getting the requested inventory information. Maybe you're not alive?")
#			
#
#
#
#
#
#
#
#	# -----------------
#	# Networking Commands
#	# -----------------
#
#	stokes = "stokes.dyndns.org"
#	chase = "chase.kicks-ass.net"
#	geoff = "24.108.77.237"
#
#	def connect(name="-NameError-", host="stokes.dyndns.org"):
#		import modules
#		modules.networking.gncore.connect(name, host)
#
#	def disconnect():
#		import modules.networking.gncore as gncore
#		import modules.gamecontrol.info as info
#		gncore.gnclient.kissGoodbye()
#		gncore.gnclient.terminate()
#		info.set("offline")
#		output("You've disconnected from the server, and you're now offline.")
#
#	def text(msg="Hi."):
#		import modules
#		modules.networking.gncore.text(msg)








# -----------------
# Notification Commands
# -----------------

def notify(text="Error", time=0.0):
	"""
	Creates a note visible to the local player.
	"""
	import engine
	engine.interface.notificationSystem.requestNote(text, time)

def alert(text="Error", buttons=None):
	"""
	Creates an alert visible to the local player.
	"""
	import engine.interface
	engine.interface.alert(text, buttons)







# -----------------
# Option Commands
# -----------------

def restoreDefaults():
	"""
	Usage: defaultOptions()
		Resets the games options to the default values.
	"""
	global engine
	options = engine.interface.options
	options.saveDefaults()
	output("Options have been set to defaults. I think.")

def setSetting(key, value):
	"""
	Usage: setSetting(setting, value)
		Sets the given setting to the given value.
	"""
	global engine
	options = engine.interface.options
	r = options.setSetting(key, value)
	output("Success value: %s"%(r))

def getSetting(key):
	"""
	Usage: getSetting(setting)
		prints the value of the requested setting.
	"""
	global engine
	options = engine.interface.options
	output("Setting %s is set to %s" % (key, options.settings[key]))
	
def defaultSetting(key):
	"""
	Usage: defaultSetting(setting)
		resets the value of the requested setting to default.
	"""
	global engine
	options = engine.interface.options
	r = options.defaultSetting(key)
	output("Success value: %s"%(r))

def setControl(key, value):
	"""
	Usage: setControl(control, value)
		Sets the given control to the given value.
	"""
	global engine
	options = engine.interface.options
	r = options.setControl(key, value)
	output("Success value: %s"%(r))

def getControl(key):
	"""
	Usage: getControl(control)
		Prints the value of the requested control.
	"""
	global engine
	options = engine.interface.options
	output("Control %s is set to %s" % (key, options.controls[key]))
	
def defaultControl(key):
	"""
	Usage: defaultControl(control)
		resets the value of the requested control to default.
	"""
	global engine
	options = engine.interface.options
	r = options.defaultControl(key)
	output("Success value: %s"%(r))

def loadOptions():
	"""
	Usage: loadOptions()
		Loads the options from FPS_options.txt
	"""
	global engine
	options = engine.interface.options
	r = options.load()
	output("Success value: %s"%(r))

# -----------------
# Engine Commands
# -----------------

def exitGame():
	"""
	Quits the current game in case of failure.
	"""
	import bge
	bge.logic.endGame()
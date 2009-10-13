helpText = """
Welcome to the FPS Project's in-game terminal.
All commands are executed as Python scripts.
Use listUserCommands() for a good time.
Precede your input with "/" to designate it as a text message.
"""

# ----------------------------
# Terminal Specific Commands
# ----------------------------

def help(cmd = None):
	"""
	Usage: help(terminalCommand)
		Prints out text that should help you use the requested terminal command. If left blank, general help information is printed.
	"""
	if cmd:
		output(cmd.__doc__)
	else:
		output(helpText)

		

def output(s):
	"""
	Usage: output(string)
		prints the given value in the terminal window.
	"""
	s = str(s)
	import modules
	modules.interface.terminal.output(s)

	

def clear():
	"""
	Usage: clear()
		Clears the terminal window of all text.
	"""
	import modules
	modules.interface.terminal.clear()

	

def listUserCommands():
	"""
	Usage: listUserCommands()
		Displays a list of commands available to the user.
	"""
	import modules
	for i in dir(modules.interface.commandsUser):
		# Filter out the python module stuff so we only get our commands
		if not i.startswith("__"):
			output(i)






# ------------------------
# Informational Commands
# ------------------------
def ammo():
	"""
	Outputs the ammopile contents to the terminal.
	"""
	try:
		import modules
		localPlayer = modules.gamecontrol.localgame.players.getLocalPlayer()
		ammopile = localPlayer.inventory.ammopile
		for ammoType in ammopile.contents:
			output("   %s: %s" % (ammoType, ammopile.contents[ammoType]))
	except:
		output("Error getting the requested inventory information. Maybe you're not alive?")
		







# -----------------
# Networking Commands
# -----------------

stokes = "stokes.dyndns.org"
chase = "chase.kicks-ass.net"
geoff = "24.108.77.237"

def connect(name="-NameError-", host="stokes.dyndns.org"):
	import modules
	modules.networking.gncore.connect(name, host)

def disconnect():
	import modules.networking.gncore as gncore
	import modules.gamecontrol.info as info
	gncore.gnclient.kissGoodbye()
	gncore.gnclient.terminate()
	info.set("offline")
	output("You've disconnected from the server, and you're now offline.")

def text(msg="Hi."):
	import modules
	modules.networking.gncore.text(msg)









# -----------------
# Notification Commands
# -----------------

def notify(text="This is a notice.", time=0.0):
	import modules.interface.notes as notes
	notes.notify(text, time)









# -----------------
# Option Commands
# -----------------

def defaultOptions():
	"""
	Usage: defaultOptions()
		Resets the games options to the default values.
	"""
	import modules
	options = modules.interface.options
	options.saveDefaults()
	output("Options have been set to defaults. I think.")

	

def setSetting(key, value):
	"""
	Usage: setSetting(setting, value)
		Sets the given setting to the given value.
	"""
	import modules
	options = modules.interface.options
	r = options.setSetting(key, value)
	output("Success value: %s"%(r))

	
	
def getSetting(key):
	"""
	Usage: getSetting(setting)
		prints the value of the requested setting.
	"""
	import modules
	options = modules.interface.options
	output("Setting %s is set to %s" % (key, options.settings[key]))

	
	
def setControl(key, value):
	"""
	Usage: setControl(control, value)
		Sets the given control to the given value.
	"""
	import modules
	options = modules.interface.options
	r = options.setControl(key, value)
	output("Success value: %s"%(r))

	
	
def getControl(key):
	"""
	Usage: getControl(control)
		Prints the value of the requested control.
	"""
	import modules
	options = modules.interface.options
	output("Control %s is set to %s" % (key, options.controls[key]))

	

def loadOptions():
	"""
	Usage: loadOptions()
		Loads the options from FPS_options.txt
	"""
	import modules
	options = modules.interface.options
	r = options.load()
	output("Success value: %s"%(r))

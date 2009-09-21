helpText = """Welcome to the FPS Project's in game terminal. \
You can execute Python commands by typing them in and \
hitting enter. If the command fails to execute properly, it \
will attempt to send your input as a text message. \
You can precede your input with a forward slash (/) to \
explicitly designate your input as a python command (if it \
fails, it will not be sent as a text message, so you won't be \
embarassed when you fail).\n\nUse listUserCommands() and \
use help(command) to learn more about a specific command"""

# ----------------------------
# Terminal Specific Commands
# ----------------------------

def help(cmd = None):
	if cmd:
		output(cmd.__doc__)
	else:
		output(helpText)

def output(s):
    s = str(s)
    import modules
    modules.interface.terminal.output(s)

def fill():
    output(helpText*100)

def clear():
    import modules
    modules.interface.terminal.clear()

def listUserCommands():
	"""
	Usage: listUserCommands()
		Displays a list of commands available to the user
	"""
	import modules
	for i in dir(modules.interface.commandsUser):
		if not i.startswith("__"):
			output(i)
			
			

# -----------------
# Option Commands
# -----------------

def defaultOptions():
    import modules
    options = modules.interface.options
    options.saveDefaults()
    output("Options have been set to defaults. I think.")

def setSetting(key, value):
    import modules
    options = modules.interface.options
    r = options.setSetting(key, value)
    output("Success value: %s"%(r))
	
def getSetting(key):
	import modules
	options = modules.interface.options
	output("Setting %s is set to %s" % (key, options.settings[key]))
	
def setControl(key, value):
    import modules
    options = modules.interface.options
    r = options.setControl(key, value)
    output("Success value: %s"%(r))
	
def getControl(key):
	import modules
	options = modules.interface.options
	output("Control %s is set to %s" % (key, options.controls[key]))

def loadOptions():
    import modules
    options = modules.interface.options
    r = options.load()
    output("Success value: %s"%(r))

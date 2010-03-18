

class Class():
	helpText = """
Welcome to the FPS Project's in-game terminal.
All commands are executed as Python scripts.
Use listUserCommands() for a good time.
Precede your input with "/" to designate it as a python command or it will be sent as a text message.
"""


	def __init__(self, slab):
		self.slab = slab
		print("Terminal user commands are good.")

	# ----------------------------
	# Terminal Specific Commands
	# ----------------------------

	def help(self, cmd = None):
		"""
		Usage: help(terminalCommand)
			Prints out text that should help you use the requested terminal command. If left blank, general help information is printed.
		"""
		if cmd:
			self.output(cmd.__doc)
		else:
			self.output(self.helpText)

	def output(self, s):
		"""
		Usage: output(string)
			prints the given value in the terminal window.
		"""
		s = str(s)
		self.slab.Interface.Terminal.output(s)

	def clear(self):
		"""
		Usage: clear()
			Clears the terminal window of all text.
		"""
		self.slab.Interface.Terminal.clear()

		

	def listUserCommands(self):
		"""
		Usage: listUserCommands()
			Displays a list of commands available to the user.
		"""
		for i in dir(self.slab.Interface.Terminal.CommandsUser):
			# Filter out the python module stuff so we only get our commands
			if not i.startswith("__") and i != "slab" and i != "helpText":
				self.output(i)
				
				
				
	def setHistoryLimit(self, I):
		"""
		Usage: setHistoryLimit()
			Changes the number of items stored in the Terminal's history to the value given.
		"""
		self.slab.Interface.Terminal.History.max = I
	





#	# ------------------------
#	# Informational Commands
#	# ------------------------
#
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

	def notify(self, text="This is a notice.", time=0.0):
		self.slab.Interface.Notes.notify(text, time)









	# -----------------
	# Option Commands
	# -----------------

	def defaultOptions(self):
		"""
		Usage: defaultOptions()
			Resets the games options to the default values.
		"""
		options = self.slab.Interface.Options
		options.saveDefaults()
		self.output("Options have been set to defaults. I think.")

	def setSetting(self, key, value):
		"""
		Usage: setSetting(setting, value)
			Sets the given setting to the given value.
		"""
		options = self.slab.Interface.Options
		r = options.setSetting(key, value)
		self.output("Success value: %s"%(r))

	def getSetting(self, key):
		"""
		Usage: getSetting(setting)
			prints the value of the requested setting.
		"""
		options = self.slab.Interface.Options
		self.output("Setting %s is set to %s" % (key, options.settings[key]))

	def setControl(self, key, value):
		"""
		Usage: setControl(control, value)
			Sets the given control to the given value.
		"""
		options = self.slab.Interface.Options
		r = options.setControl(key, value)
		self.output("Success value: %s"%(r))

	def getControl(self, key):
		"""
		Usage: getControl(control)
			Prints the value of the requested control.
		"""
		options = self.slab.Interface.Options
		self.output("Control %s is set to %s" % (key, options.controls[key]))

	def loadOptions(self):
		"""
		Usage: loadOptions()
			Loads the options from FPS_options.txt
		"""
		options = self.slab.Interface.Options
		r = options.load()
		self.output("Success value: %s"%(r))

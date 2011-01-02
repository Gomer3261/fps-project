### Interface Module ###

class initializeInterface:
	def __init__(self):
	
		import engine.interface.bgui
		self.bgui = bgui
		
		import engine.interface.inputs as inputsModule
		self.inputs = inputsModule.initializeInputs()
		
		import engine.interface.options as optionsModule
		self.options = optionsModule.initializeOptions(self.inputs)
		
		import engine.interface.terminal as terminalModule
		self.terminal = terminalModule.initializeTerminal(self.bgui)

#		import Notes as NotesModule
#		self.Notes = NotesModule.Class()

	def main(self):
		self.terminal.main()

	#Quick input detection
	def checkControl(self, control):
		return self.inputs.controller.isPositive(control)
		
	def controlStatus(self, control):
		return self.inputs.controller.getStatus(control)
		
	#Quick option access
	def defaultOptions(self):
		return self.options.saveDefaults()
		
	def setSetting(self, setting, value):
		return self.options.setSetting(self, setting, value)
		
	def getSetting(self, setting):
		return self.options.getSetting(self, setting)
		
	def resetSetting(self, setting):
		return self.options.defaultSetting(setting)
		
	def setControl(self, control, value):
		return self.options.setSetting(self, control, value)
		
	def getControl(self, control):
		return self.options.getSetting(self, control)
		
	def resetControl(self, control):
		return self.options.defaultControl(control)

#	def run(self, Network, GameState):
#		"""
#		handles controlling the terminal scene.
#		"""
#		self.Terminal.handleOpenClose()
#		self.handleTexts(Network, GameState)
#	
#	def handleTexts(self, Network, GameState):
#		for bundle in Network.inBundles:
#			fwdUID, item = bundle
#			flag, data = item
#			if flag == 'TXT':
#				UID, text = data
#				self.displayText(UID, text, GameState)
#				if Network.GPS: Network.GPS.sendToAll( ('TXT', (UID, text)) )
#	
#	def displayText(self, UID, text, GameState):
#		if UID:
#			name = GameState.getUserName(UID)
#			self.out("%s: %s"%(name, text), note=True)
#		else:
#			self.out(text, note=True)
#	
	def out(self, text, terminal=True, note=False, console=False):
		"""
		Basic output method. Outputs to the terminal by default.
		"""
		if terminal:
			self.terminal.output(text)
		if note:
			pass
		if console:
			print(text)
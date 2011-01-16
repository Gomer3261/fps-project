### Interface Module ###
# Maintained by:
# Geoffrey Gollmer (Gomer)

class initializeInterface:
	def __init__(self):
		"""
		Initialization function for the intferface object.
		Initializes Interface's components.
		"""
		#Bgui is an external library, courtesy of Mitchell Stokes. Thanks Mitchell
		import engine.interface.bgui
		self.bgui = bgui
		
		import engine.interface.inputs as inputsModule
		self.inputs = inputsModule.initializeInputs()
		
		import engine.interface.options as optionsModule
		self.options = optionsModule.initializeOptions(self.inputs)
		
		import engine.interface.terminal as terminalModule
		self.terminal = terminalModule.initializeTerminal(self.bgui)
		
		import engine.interface.notes as notesModule
		self.notificationSystem = notesModule.initializeNotificationSystem(self, self.bgui)

	def main(self):
		"""
		Main interface loop.
		"""
		import bge
		self.terminal.main()
		self.notificationSystem.main()
		bge.logic.getCurrentScene().post_draw = [self.render]
		
		if bge.logic.keyboard.events[bge.events.TABKEY] == bge.logic.KX_INPUT_JUST_ACTIVATED:
			self.alert("Are you sure you want to exit the game?", (("Exit", self._endGame), ("Resume", None)))
		
	def render(self):
		"""
		Renders the components of the interface using post_draw.
		"""
		self.notificationSystem.renderNote()
		if self.terminal.active:
			self.terminal.render()
		#self.menus.render()
		self.notificationSystem.renderAlert()
		#self.debugDisplay.render()
		
	#InterfaceCommands:
	def output(self, text, terminal=True, note=False, console=False):
		"""
		outputs information.
		first argument is a string to be output
		last 3 optional arguments choose which form of output to use.
		they are in the order: terminal, note, console
		"""
		if terminal: self.terminal.output(text)
		if note: self.notificationSystem.requestNote(text)
		if console: print(text)
		
	def alert(self, text, buttons):
		"""
		Creates an alert using the notificationSystem.
		"""
		self.notificationSystem.requestAlert(text, buttons)
		
	def terminalIsActive(self):
		"""
		Checks if the terminal is currently active.
		"""
		import engine
		return engine.interface.terminal.active
	
	
	
	
	
	
	
	
	#Quick input detection:
	@property
	def mouse(self):
		return self.inputs.mouse
	
	def isControlPositive(self, control):
		"""
		Function to check if a control is active (positive).
		"""
		return self.inputs.controller.isPositive(control)
		
	def getControlStatus(self, control):
		"""
		Function to retrieve a control's status.
		0=inactive,
		1=just activated,
		2=active,
		3=just deactivated 
		"""
		return self.inputs.controller.getStatus(control)
	
	
	
	
	
	
	
	#Quick option access:
	def defaultOptions(self):
		"""
		Function to reset controls and settings to default.
		"""
		return self.options.saveDefaults()
		
	def setSetting(self, setting, value):
		"""
		Function to set individual settings.
		"""
		return self.options.setSetting(setting, value)
		
	def getSetting(self, setting):
		"""
		Function to retrieve individual settings.
		"""
		return self.options.getSetting(setting)
		
	def resetSetting(self, setting):
		"""
		Function to reset indivdual settings to their default values.
		"""
		return self.options.defaultSetting(setting)
		
	def setControl(self, control, value):
		"""
		Function to set individual controls.
		"""
		return self.options.setSetting(control, value)
		
	def getControl(self, control):
		"""
		Function to retrieve individual controls.
		"""
		return self.options.getSetting(self, control)
		
	def resetControl(self, control):
		"""
		Function to reset individual controls to their default values.
		"""
		return self.options.defaultControl(control)


	#Callbacks
	def _endGame(self, button):
		import bge
		bge.logic.endGame()
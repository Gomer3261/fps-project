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
		
		#Notes to be added once it's converted to bgui.
#		import Notes as NotesModule
#		self.Notes = NotesModule.Class()

	def main(self):
		"""
		Main interface loop.
		"""
		self.terminal.main()
		#self.notes.main() 
		
	#InterfaceCommands:
	def out(self, text, terminal=True, note=False, console=False):
		"""
		Basic output method. Outputs to the terminal by default.
		"""
		if terminal:
			self.terminal.output(text)
		if note:
			pass
			#self.notes.output(text)
		if console:
			print(text)
			
	def isTerminalActive():
		"""
		Checks if the terminal is currently active.
		"""
		return engine.interface.terminal.active

	#Quick input detection:
	@property
	def mouse(self):
		return self.inputs.mouse
	
	def checkControl(self, control):
		"""
		Function to check if a control is active (positive).
		"""
		return self.inputs.controller.isPositive(control)
		
	def controlStatus(self, control):
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
		return self.options.setSetting(self, setting, value)
		
	def getSetting(self, setting):
		"""
		Function to retrieve individual settings.
		"""
		return self.options.getSetting(self, setting)
		
	def resetSetting(self, setting):
		"""
		Function to reset indivdual settings to their default values.
		"""
		return self.options.defaultSetting(setting)
		
	def setControl(self, control, value):
		"""
		Function to set individual controls.
		"""
		return self.options.setSetting(self, control, value)
		
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



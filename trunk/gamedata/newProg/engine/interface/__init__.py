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
		import bge
		self.terminal.main()
		bge.logic.getCurrentScene().post_draw = [self.render]
		
		#self.notes.main() 
		
	def render(self):
		"""
		Renders the components of the interface using post_draw.
		"""
		if self.terminal.active:
			self.terminal.render()
		
	#InterfaceCommands:
	def output(self, text, terminal=True, note=False, console=False):
		if terminal: self.terminal.output(text)
		if note: pass
		if console: print(text)
			
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



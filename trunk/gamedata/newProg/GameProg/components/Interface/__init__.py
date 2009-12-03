### Interface Component ###

class Class:
	def __init__(self):
		
		import Inputs as InputsModule
		self.Inputs = InputsModule.Class()
		
		import Options as OptionsModule
		self.Options = OptionsModule.Class(self.Inputs)
		
		import Terminal as TerminalModule
		self.Terminal = TerminalModule.Class()
	
	def run(self):
		self.Terminal.handleOpenClose()

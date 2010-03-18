### Interface Component ###

class Class:
	def __init__(self):
		
		import Inputs as InputsModule
		self.Inputs = InputsModule.Class()
		
		import Options as OptionsModule
		self.Options = OptionsModule.Class(self.Inputs)
		
		import Terminal as TerminalModule
		self.Terminal = TerminalModule.Class()
		
		import Notes as NotesModule
		self.Notes = NotesModule.Class()
		
		print("Interface -- check.")
	
	def run(self):
		self.Terminal.handleOpenClose()
	
	def terminalOutputWithNotification(self, string, time=None):
		"""
		Outputs a string to the terminal AND makes a notification of the string.
		"""
		self.Terminal.output(string)
		self.Notes.notify(string, time)
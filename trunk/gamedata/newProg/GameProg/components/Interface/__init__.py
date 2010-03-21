### Interface Component ###

class Class:
	def __init__(self, slab):
		self.slab = slab
		
		import Inputs as InputsModule
		self.Inputs = InputsModule.Class()
		
		import Options as OptionsModule
		self.Options = OptionsModule.Class(self.Inputs)
		
		import Terminal as TerminalModule
		self.Terminal = TerminalModule.Class(slab)
		
		import Notes as NotesModule
		self.Notes = NotesModule.Class()
		
		print("Interface -- check.")
	
	def run(self):
		"""
		handles controlling the terminal scene.
		"""
		self.Terminal.handleOpenClose()
	
	def out(self, text, terminal=True, note=False, console=False):
		"""
		Basic output method. Outputs to the terminal, and to notifications by default.
		"""
		if terminal:
			self.Terminal.output(text)
		if note:
			self.Notes.notify(text)
		if console:
			print(text)
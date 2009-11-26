### Interface Component ###

class Class:
	def __init__(self):
		
		import Inputs as InputsModule
		self.Inputs = InputsModule.Class()
		
		import Options as OptionsModule
		self.Options = OptionsModule.Class(Inputs)
		
	def run(self):
		pass

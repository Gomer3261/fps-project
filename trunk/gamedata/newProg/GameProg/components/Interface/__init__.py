### Interface Component ###

class Class:
	def __init__(self):
		
		import inputs as inputsModule
		self.inputs = inputsModule.Class()
		
		import options as optionsModule
		self.options = optionsModule.Class(inputs)
		
	def run(self):
		pass

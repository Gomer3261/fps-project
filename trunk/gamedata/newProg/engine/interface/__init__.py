### Interface Module ###

class initializeInterface:
	def __init__(self):
		
		import engine.interface.inputs as inputsModule
		self.inputs = inputsModule.initializeInputs()
		
		import engine.interface.options as optionsModule
		self.options = optionsModule.initializeOptions(self.inputs)
		
#		import terminal as terminalModule
#		self.terminal = terminalModule.initializeTerminal()
#		
#		import Notes as NotesModule
#		self.Notes = NotesModule.Class()
#		
#		print("Interface -- check.")
#	
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
#	def out(self, text, terminal=True, note=False, console=False):
#		"""
#		Basic output method. Outputs to the terminal by default.
#		"""
#		if terminal:
#			self.Terminal.output(text)
#		if note:
#			self.Notes.notify(text)
#		if console:
#			print(text)
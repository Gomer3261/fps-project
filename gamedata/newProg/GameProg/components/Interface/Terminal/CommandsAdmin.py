
class Class():
	def __init__(self, slab):
		self.slab = slab
		print("Terminal admin commands look good.")

	def gs(self):
		"""
		Outputs the current gamestate information to the terminal.
		"""
		interface = self.slab.Interface
		gamestate = self.slab.GameState
		Interface.out( str(gamestate.contents), 1, 0 )
	
	def endServer(self):
		self.slab.Network.endServer()

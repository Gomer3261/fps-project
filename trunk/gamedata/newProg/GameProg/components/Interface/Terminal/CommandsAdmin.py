
class Class():
	def __init__(self, slab):
		self.slab = slab
		print("Terminal admin commands look good.")

	def gs(self):
		"""
		Outputs the current gamestate information to the terminal.
		"""
		self.slab.Interface.out( str(self.slab.GameState.contents), 1, 0 )
	
	def endServer(self):
		self.slab.Network.endServer()
	
	def startServer(self, address=None):
		if not address:
			import GameLogic
			GI = GameLogic.globalDict['gameInfo']
			address = GI['hostaddress']
		self.slab.Network.startServer(address, self.slab.Interface)
	
	def startClient(self, address=None):
		if not address:
			import GameLogic
			GI = GameLogic.globalDict['gameInfo']
			address = GI['address']
		self.slab.Network.startClient(address)
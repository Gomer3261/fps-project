
class Class():
	def __init__(self, slab):
		self.slab = slab
		print("Terminal admin commands look good.")

	def fullgs(self):
		"""
		Outputs the current gamestate information to the terminal.
		"""
		self.slab.Interface.out( str(self.slab.GameState.contents), console=True )
	
	def gs(self):
		for EID in self.slab.GameState.contents['E']:
			self.slab.Interface.out( str(EID), console=True )
	
	def lg(self):
		for EID in self.slab.LocalGame.entities:
			self.slab.Interface.out( str(EID), console=True )
	
	def sessions(self):
		self.slab.Interface.out( str(self.slab.Network.GPS.tcpServer.sessionStorage.sessions) )
	
	def endServer(self):
		self.slab.Network.endServer()
	
	def startServer(self, address=None):
		if not address:
			import bge
			GI = bge.logic.globalDict['gameInfo']
			address = GI['hostaddress']
		self.slab.Network.startServer(address, self.slab.Interface)
	
	def startClient(self, address=None):
		if not address:
			import bge
			GI = bge.logic.globalDict['gameInfo']
			address = GI['address']
		self.slab.Network.startClient(address)
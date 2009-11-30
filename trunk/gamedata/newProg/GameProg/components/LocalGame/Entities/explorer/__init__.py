### Explorer Entity ###

class Class:
	def __init__(self, EID, LocalGame):
		self.EID = EID
		self.LocalGame = LocalGame
		self.GameState = LocalGame.GameState
		self.Networking = LocalGame.Networking
		self.Interface = LocalGame.Interface
		
		# Initiating the gameObj
		import GameLogic as gl
		own = gl.getCurrentController().owner
		self.gameObj = gl.getCurrentScene().addObject("explorer", own)
		
		print("\nExplorer Initiated.\n")
	
	def end(self):
		print("\nExplorer Entity Ended.\n")
		self.gameObj.endObject()
		self.gameObj = None
	
	def run(self):
		pass
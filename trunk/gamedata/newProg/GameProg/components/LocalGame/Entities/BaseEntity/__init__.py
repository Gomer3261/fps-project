### Base Entity ###

class Class:
	def __init__(self, EID, LocalGame):
		self.EID = EID
		
		self.LocalGame = LocalGame
		self.GameState = LocalGame.GameState
		self.Networking = LocalGame.Networking
		
	
	def run(self):
		EID = self.EID
		
		LocalGame = self.LocalGame
		GameState = self.GameState
		Networking = self.Networking
	
	
		entityData = GameState.getEntity(EID)
		entityDataOut = {}
		
		package = entityDataOut
		Networking.gpsnet.send(package) # TCP
		Networking.gpsnet.throw(package) # UDP

### Base Entity ###

class Class:
	def __init__(self, ID, LocalGame):
		self.ID = ID
		
		self.LocalGame = LocalGame
		self.GameState = LocalGame.GameState
		self.Networking = LocalGame.Networking
		
	
	def run(self):
		ID = self.ID
		
		LocalGame = self.LocalGame
		GameState = self.GameState
		Networking = self.Networking
	
	
		entityData = GameState.getEntity(ID)
		entityDataOut = {}
				
		value = entityData["D"]["V"]
		value += 1
		
		entityDataOut["D"]["V"] = value
		
		package = entityDataOut
		Networking.gpsnet.send(package) # TCP
		Networking.gpsnet.throw(package) # UDP

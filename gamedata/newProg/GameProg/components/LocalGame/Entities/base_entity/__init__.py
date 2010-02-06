### Base Entity ###

class Class:
	def __init__(self, EID, LocalGame):
		self.type = "base_entity"
		self.EID = EID
		
		self.LocalGame = LocalGame
		self.GameState = LocalGame.GameState
		self.Networking = LocalGame.Networking
		self.Interface = LocalGame.Interface
	
	def run(self):
		pass
		#entityData = GameState.getEntity(self.EID)
		#entityDataOut = {}
		#package = entityDataOut
		#Networking.gpsnet.send(package) # TCP
		#Networking.gpsnet.throw(package) # UDP
### Base Entity ###

class Class:
	def __init__(self, EID, LocalGame):
		self.EID = EID
		
		self.LocalGame = LocalGame
		self.GameState = LocalGame.GameState
		self.Networking = LocalGame.Networking
		self.Interface = LocalGame.Interface
		
		import GameLogic as gl
		own = gl.getCurrentController().owner
		self.obj = gl.getCurrentScene().addObject("test", own)
		
		changes = {"T":0}
		package = ['GS', ['EC', [EID, changes]]]
		Networking.gpsnet.send(package)
		
		print("Test Entity Created\n\n")
		
	
	def run(self):
		EID = self.EID
		
		LocalGame = self.LocalGame
		GameState = self.GameState
		Networking = self.Networking
		Interface = self.Interface
		
		entityData = GameState.getEntity(EID)
	
		if entityData["CD"]["T"] < 50:
			tick = entityData["CD"]["T"] + 1
			
			#updating GameState
			changes = {"T":tick}
			package = ['GS', ['EC', [EID, changes]]]
			Networking.gpsnet.send(package)
			
		else:
			#ending the object
			package = ['GS', ['AR', ['RE', EID]]]
			Networking.gpsnet.send(package)
			self.obj.endObject()
		
		entityData = GameState.getEntity(EID)
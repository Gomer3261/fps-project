### Test Entity ###

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
		self.gameObj = gl.getCurrentScene().addObject("test", own)
		
		# Initiating the CD (Controlled Data)
		changes = {"T":0}
		package = ['GS', ['EC', [EID, changes]]]
		self.Networking.gpsnet.send(package)
		
		print("\nTest Entity Initiated.\n")
	
	def end(self):
		print("Entity(%s).end()"%(self.EID))
		self.gameObj.endObject()
		self.gameObj = None
	
	def run(self):
		entityData = self.GameState.getEntity(self.EID)
		
		try: # If there is an error with getting the 'T' (Tick) variable from GameState Contents... (see except)
			if entityData["CD"]["T"] < 50:
				tick = entityData["CD"]["T"] + 1
				
				# Updating the Controlled Data (with the Tick)
				changes = {"T":tick}
				package = ['GS', ['EC', [self.EID, changes]]]
				self.Networking.gpsnet.send(package)
				
			else:
				# Asking to remove the entity.
				package = ['GS', ['AR', ['RE', self.EID]]]
				self.Networking.gpsnet.send(package)
		except: # Then we'll re-initiate the Tick. This will definitely result in a double initiation, but I don't really give a fuck.
			changes = {"T":0}
			package = ['GS', ['EC', [self.EID, changes]]]
			self.Networking.gpsnet.send(package)
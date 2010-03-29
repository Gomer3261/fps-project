### Spawnpoint ###
import base_entity

class Class(base_entity.Class):
	type = "spawnpoint"
	
	def initiateGameStateData(self):
		"""
		Initiates the GameState OwnerData and ControllerData for this entity.
		"""
		import time
		
		OD = {}
		
		CD = {}
		CD['P'] = [0.0, 0.0, 0.0] # Position
		CD['O'] = None # Orientation
		
		self.sendData('OD', None, OD)
		self.sendData('CD', None, CD)
	
	def initiate(self):
		ARGS = self.getOD()['ARGS']
		
		# Initiate gameObject
		import GameLogic as gl
		own = gl.getCurrentController().owner
		self.gameObject = gl.getCurrentScene().addObject("spawnpoint", own)
		self.gameObject["EID"] = self.EID
		self.gameObject.position = ARGS['P']
	
	def getSpawnPosition(self):
		x, y, z = self.gameObject.position
		return [x, y, (z+2.0)]
	
	def end(self):
		self.gameObject.endObject()

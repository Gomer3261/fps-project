### Box ###
import base_entity

class Class(base_entity.Class):
	type = "box"
	
	def initiateGameStateData(self):
		"""
		Initiates the GameState OwnerData and ControllerData for this entity.
		"""
		import time
		
		OD = self.getOD()
		
		CD = {}
		CD['P'] = [0.0, 0.0, 0.0] # Position
		CD['O'] = None # Orientation
		
		self.sendData('OD', None, OD)
		self.sendData('CD', None, CD)
	
	def initiate(self):
		ARGS = self.getOD()['ARGS']
		
		# Initiate gameObject
		import bge
		own = bge.logic.getCurrentController().owner
		self.gameObject = bge.logic.getCurrentScene().addObject("box", own)
		self.gameObject["EID"] = self.EID
		self.gameObject.position = ARGS['P']
		self.gameObject.alignAxisToVect(ARGS['R'], 1)
	
	def end(self):
		self.gameObject.endObject()
		self.gameObject = None
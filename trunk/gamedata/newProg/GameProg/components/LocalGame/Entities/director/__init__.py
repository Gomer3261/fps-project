### Director Entity ###
import base_entity

class Class(base_entity.Class):
	type = "director"
	
	def initiateGameStateData(self):
		"""
		Initiates the GameState OwnerData and ControllerData for this entity.
		"""
		import time
		
		OD = {}
		OD["gameplay"] = True
		
		CD = {}
		CD["gameTimeStart"] = time.time()
		CD["gameTime"] = 0.0
		
		self.setOD(OD)
		self.setCD(CD)
	
	def getCurrentGameTime(self):
		start = self.getCD()['gameTimeStart']
		import time
		return time.time()-start

	def controllerDataSimulate(self):
		"""
		Simulates controller data, and updates the changes to the GameState via Networking.
		"""
		gameTime = self.getCurrentGameTime()
		self.Networking.gpsnet.throw( ['GS', ['EM', [(self.EID, 'CD', 'gameTime', gameTime)]]] )
		#self.setCDV("gameTime", gameTime)
	
	def alwaysRun(self):
		CD = self.getCD()
		print("Director:CD['gameTime']: %.2f"%(CD['gameTime']))
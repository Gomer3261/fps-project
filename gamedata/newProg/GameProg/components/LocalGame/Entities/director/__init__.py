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
		
		self.sendData('OD', None, OD)
		self.sendData('CD', None, CD)
	
	
	
	def getCurrentGameTime(self):
		try:
			start = self.getCD()['gameTimeStart']
			import time
			return time.time()-start
		except:
			pass
	
	
	
	def spawnControl(self):
		"""
		Allows anybody connected to this director (as a client, or owner) to send spawn requests.
		"""
		if not self.Interface.Terminal.active:
			s = self.Interface.Inputs.Controller.getStatus('spawn')
			if s==3:
				self.Networking.gpsnet.send(['GS', ['AR', ['SE', 'nanoshooter']]])
	

	def controllerDataSimulate(self):
		"""
		Simulates controller data, and updates the changes to the GameState via Networking.
		"""
		gameTime = self.getCurrentGameTime()
		self.throwData('CD', 'gameTime', gameTime)
	
	
	
	
	def alwaysRun(self):
		try:
			self.spawnControl()
			#CD = self.getCD()
			#print("Director:CD['gameTime']: %.2f"%(CD['gameTime']))
		except:
			pass
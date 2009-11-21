### Networking Component ###

class Class:
	def __init__(self, cont):
	
		import msnet as msnetModule
		self.msnet = msnetModule.Class()
		
		import gpsnet as gpsnetModule
		self.gpsnet = gpsnetModule.Class()
		
	def run(self, MasterInfo):
		"""
		Runs networking operations for the master server
		and the gameplay server.
		"""
		self.msnet.run(MasterInfo)
		self.gpsnet.run(MasterInfo)

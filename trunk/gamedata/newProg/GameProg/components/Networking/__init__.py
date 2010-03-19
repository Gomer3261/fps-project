### Networking Component ###

class Class:
	def __init__(self, slab):
		import comms; self.comms = comms
		import classes; self.classes = classes
	
		import msnet as msnetModule
		self.msnet = msnetModule.Class()
		
		import gpsnet as gpsnetModule
		self.gpsnet = gpsnetModule.Class(slab)
		
		print("Networking's ready.")
		
	def run(self, MasterInfo):
		"""
		Runs networking operations for the master server
		and the gameplay server.
		"""
		self.msnet.run(MasterInfo)
		self.gpsnet.run(MasterInfo)

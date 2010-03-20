### Networking Component ###

class Class:
	def __init__(self, slab):
		self.inBundles = []
		self.sendOutBuffer = []
		self.throwOutBuffer = []
	
		import comms; self.comms = comms
		import classes; self.classes = classes
	
		import msnet as msnetModule
		self.msnet = msnetModule.Class()
		
		import gpsnet as gpsnetModule
		self.gpsnet = gpsnetModule.Class(slab)
		
		print("Networking's ready.")
		
	def run(self, Admin, Interface):
		"""
		Maintains GPS and GPC by running them. If they exist, that is.
		"""
		pass
	
	def incoming(self):
		"""
		If there is a GPS or GPC, or both, we receive bundles from them and plop them into
		inBundles.
		"""
		pass
	
	def outgoing(self):
		"""
		Sends/throws all of the items in the out buffers to the Host.
		If we are the host, then we just plop them straight into inBundles.
		If we're not the host, then we send them through the GPC (GamePlayClient).
		"""
		pass
	
	def send(self, item):
		"""
		Puts an item in the outgoing buffer.
		"""
		self.sendOutBuffer.append(item)
	
	def throw(self, item):
		"""
		Puts an item in the outgoing buffer.
		"""
		self.throwOutBuffer(item)
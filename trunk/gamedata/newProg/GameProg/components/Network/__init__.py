### Networking Component ###

class Class:
	import comms
	import classes
	import core
	
	def __init__(self, slab):
		self.inBundles = []
		self.sendOutBuffer = []
		self.throwOutBuffer = []
		
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
	
	def outgoing(self, Admin, GameState):
		"""
		Sends/throws all of the items in the out buffers to the Host.
		If we are the host, then we just plop them straight into inBundles.
		If we're not the host, then we send them through the GPC (GamePlayClient).
		"""
		weAreHost = False
		if Admin.UID == GameState.getHost():
			weAreHost = True
		
		if weAreHost:
			# We just have to turn each item in the outgoing buffers, convert them into bundles
			# and then plop them right into the in buffer. Then clear the outgoing buffers.
			for item in self.sendOutBuffer:
				bundle = (Admin.UID, item)
				self.inBundles.append(bundle)
			for item in self.throwOutBuffer:
				bundle = (Admin.UID, item)
				self.inBundles.append(bundle)
			self.sendOutBuffer = []
			self.throwOutBuffer = []
		
		else:
			# We have to send/throw our crap through the GPC.
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
		self.throwOutBuffer.append(item)
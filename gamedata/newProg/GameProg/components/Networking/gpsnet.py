### GameplayServer Networking Module ###

class Class:
	"""
	GPS Net
	"""

	def __init__(self):
		connected = 0
		blank = None
	
	
	### ================================================
	### Run Method
	### ================================================
	
	def run(self, MasterInfo):
		pass
	
	
	def handleIn(self):
		"""
		Handles data that's in the inBuffer.
		"""
		pass
	
	def send(self, data):
		"""
		Adds data to the outBuffer.
		"""
		pass
	
	def handleOut(self):
		"""
		Sends the data in the outBuffer through the socket, retaining the leftovers to try
		again next run.
		"""
		pass

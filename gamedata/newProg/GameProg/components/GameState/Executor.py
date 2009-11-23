### GameState.Executor ###
# Perhaps should be renamed to "Interpreter"?

class Class:
	"""
	Interprets requests to make changes to the GameState.
	"""
	
	def __init__(self):
		pass
	
	def run(self, GameState, gpsnet):
		"""
		Grabs inbound packages from the gpsnet,
		handles them with handleRequest().
		"""
		packages = gpsnet.getInPackages()
		for package in packages:
			if package[0] == "r":
				# Is a request
				self.handleRequest(package[1], GameState, gpsnet)
	
	
	
	
	def handleRequest(self, request, GameState, gpsnet):
		"""
		Interprets a request to change the GameState.
		"""
		pass
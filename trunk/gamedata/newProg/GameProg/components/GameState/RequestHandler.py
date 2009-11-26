### GameState.RequestHandler ###

class Class:
	"""
	Interprets requests to make changes to the GameState.
	GameState Request Protocol:
	
	Entity Control Request:
		['EC', [58, changes] ] # EC flag for EntityControl. 58 is the EID of the entity we are attempting to contol.
		changes = { "P":[1.1, 5.6, 1.0] } # changing the position...
		
		Entity Control requests are used when a user wants to control variables of an entity.
		A good example if this would be a user controlling their player entity; they are not 
		the owner of the player entity, but they can use EC requests to control certain variables
		of the entity (like position and such).
	
	
	Action Request:
		['AR', action] # 'AR' flag obviously for ActionRequest.
		action = ['DMG', 52, 23] # this would be a request to apply 23 damage to player entity 52.
		
		An Action Request is fairly broad, and is used to request an action that may require
		some computation of the GameState.
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
### LocalGame.RequestHandler ###

class Class:
	"""
	LocalGame RequestHandler
	"""
	
	def __init__(self):
		print("  LocalGame RequestHandler is ready.")
		pass
	
	def run(self, LocalGame, gpsnet):
		"""
		Grabs inbound packages from the gpsnet,
		handles them with handleRequest().
		"""
		items = gpsnet.inItems
		#print("\ninItems: %s\n"%(items))
		for item in items:
			sender, package = item
			packageFlag, request = package
			if packageFlag == 'LG':
				self.handleRequest(sender, request, LocalGame, gpsnet)
		#if items: print("\nGameState Changed!: %s\n"%(GameState.contents))
	
	
	
	
	def handleRequest(self, sender, request, LocalGame, gpsnet):
		"""
		Interprets a request made to the LocalGame
		"""
		try:
			flag, data = request
			
			if flag == 'MEMO':
				self.handleEntityMemoRequest(request, sender, LocalGame, gpsnet)
		except:
			import traceback; traceback.print_exc()
	
	
	
	
	
	def handleEntityMemoRequest(self, request, sender, LocalGame, gpsnet):
		"""
		Handles a MEMO Request.
		('LG', ('MEMO', (EID, memoData)))
		"""
		flag, memo = request
		EID, memoData = memo
		LocalGame.giveMemo(EID, memoData)

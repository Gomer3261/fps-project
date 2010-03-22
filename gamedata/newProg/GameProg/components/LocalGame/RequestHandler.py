### LocalGame.RequestHandler ###

class Class:
	"""
	LocalGame RequestHandler
	"""
	
	def __init__(self):
		print("  LocalGame RequestHandler is ready.")
		pass
	
	def run(self, LocalGame, Network):
		"""
		Grabs inbound packages from the gpsnet,
		handles them with handleRequest().
		"""
		for bundle in Network.inBundles:
			senderUID,item=bundle; flag,data=item
			if flag == 'LG':
				self.handleRequest(bundle, LocalGame, Network)
		#if items: print("\nGameState Changed!: %s\n"%(GameState.contents))
	
	
	
	
	def handleRequest(self, bundle, LocalGame, Network):
		"""
		Interprets a request made to the LocalGame
		"""
		try:
			senderUID,item=bundle; flag,data=item
			request=data; requestFlag,requestData=request
			
			if requestFlag == 'MEMO':
				self.handleEntityMemoRequest(bundle, LocalGame, Network)
		except:
			import traceback; traceback.print_exc()
	
	
	
	
	
	def handleEntityMemoRequest(self, bundle, LocalGame, Network):
		"""
		Handles a MEMO Request.
		('LG', ('MEMO', (EID, memoData)))
		"""
		senderUID,item=bundle; flag,data=item
		request=data; requestFlag,requestData=request
		
		EID, memoData = requestData
		LocalGame.giveMemo(EID, memoData)

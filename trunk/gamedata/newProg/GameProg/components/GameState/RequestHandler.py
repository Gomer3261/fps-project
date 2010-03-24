### GameState.RequestHandler ###

class Class:
	"""
	Interprets requests to make changes to the GameState.
	GameState Request Protocol:
	
	Full Distro
		('GS', ('FD', contents))
	
	Shout Distro
		('GS', ('SD', shouts))
	
	Entity Mod Item:
		('GS', ('EM', changes))
		('EM', changes)
		changes = [change, change2, change3...]
		change = (EID, type, key, value)
		change = (69, 'CD', 'position', [0.0, 0.0, 0.0])
		('EM', [(EID, type, key, value)])
	
	
	Action Request Item:
		***
		Damaging players might be done with memos, we'll see...
		***
		('AR', action) # 'AR' flag obviously for ActionRequest.
		action = ('DMG', 52, 23) # this would be a request to apply 23 damage to player entity 52.
		action = ('SP', 69, 12) #DEPRECATED!USE-BELOW! This would spawn a player entity with control given to UID 69.
		action = ('SE', (entityType, (ownerUID, controllerUID), [arg_position, arg_rotation, arg_somethingElse...]))
		
		An Action Request is fairly broad, and is used to request an action that may require
		some computation of the GameState.
	"""
	
	def __init__(self):
		self.shouts = []
		print("  GameState's Request Handler ready.")
		pass
	
	def run(self, GameState, Network):
		"""
		Grabs inbound bundles from the Network,
		handles them with handleRequest().
		"""
		bundles = Network.inBundles
		for bundle in bundles:
			senderUID,item=bundle; flag,data=item
			if flag == 'GS':
				self.handleRequest(bundle, GameState, Network)
	
	
	
	
	def handleRequest(self, bundle, GameState, Network):
		"""
		Interprets a request to change the GameState.
		"""
		try:
			senderUID,item=bundle; flag,data=item
			request=data; requestFlag,requestData=request
			
			if requestFlag == 'EM': # Entity Mod
				self.handleEntityModRequest(bundle, GameState, Network)
			
			if requestFlag == 'AR': # Action Request
				self.handleActionRequest(bundle, GameState, Network)
			
			if requestFlag == 'FD': # Full Distro
				print("GS Request Handler: GOT FD!")
				self.handleFullDistroRequest(bundle, GameState, Network)
			
			if requestFlag == 'SD': # Shout Distro
				for shout in requestData:
					self.handleRequest(bundle, GameState, Network) # Holy recursive batman!
		except:
			import traceback; traceback.print_exc()
	
	
	
	def handleFullDistroRequest(self, bundle, GameState, Network):
		"""
		Handles an FD Request.
		('GS', ('FD', contents))
		"""
		senderUID,item=bundle; flag,data=item
		request=data; requestFlag,requestData=request
		
		newGameStateContents = requestData
		GameState.applyNewContents(newGameStateContents)
	
	def handleEntityModRequest(self, bundle, GameState, Network):
		"""
		Handles an EM Request.
		('GS', ('EM', changes))
		"""
		senderUID,item=bundle; flag,data=item
		request=data; requestFlag,requestData=request
		
		changes = requestData
		for change in changes:
			EID, type, key, value = change
			if key:
				GameState.contents['E'][EID][type][key] = value
			else:
				GameState.contents['E'][EID][type] = value
		self.shouts.append(bundle)

	
	def handleActionRequest(self, bundle, GameState, Network):
		"""
		Handles an Action Request.
		"""
		#print("ACTION")
		senderUID,item=bundle; flag,data=item
		request=data; requestFlag,requestData=request
		
		actionFlag, actionData = requestData
		
		if actionFlag == "SE": # Spawn Entity...
			#print("SPAWNING ENTITY")
			# ( entityType, (ownerID, controllerID), [arg_position, arg_rotation, arg_somethingElse...] )
			type, UIDs, args = actionData
			ownerUID, controllerUID = UIDs
			EID = GameState.addEntity(type, ownerUID, controllerUID, args)
			# We'll let this information be distributed in a full GS distro.
		
		if actionFlag == "RE": # Remove Entity
			EID = actionData
			GameState.removeEntity(EID)
			# We'll let this information be distributed in a full GS distro.
		
		if actionFlag == 'AU': # Add User
			# Likely not handled this way... Maybe deprecated?
			ticket, name = actionData
			UID = GameState.addUser(ticket, name)
			# We'll let this information be distributed in a full GS distro.
		
	

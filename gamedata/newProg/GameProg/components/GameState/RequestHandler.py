### GameState.RequestHandler ###

class Class:
	"""
	Interprets requests to make changes to the GameState.
	GameState Request Protocol:
	
	Entity Mod Request:
		('EM', changes)
		changes = [change, change2, change3...]
		change = (EID, type, key, value)
		change = (69, 'CD', 'position', [0.0, 0.0, 0.0])
		('EM', [(EID, type, key, value)])
	
	Value Append Request:
		*** DEPRECATED I THINK ***
		('VA', EID, 'CD', 'someKindOfQueue', [valuesToAppend])
	
	
	Action Request:
		***
		Damaging players might be done with memos, we'll see...
		***
		('AR', action) # 'AR' flag obviously for ActionRequest.
		action = ('DMG', 52, 23) # this would be a request to apply 23 damage to player entity 52.
		action = ('SP', 69, 12) #DEPRECATED!USE-BELOW! This would spawn a player entity with control given to UID 69.
		action = ('SE', (entityType, (ownerID, controllerID), [arg_position, arg_rotation, arg_somethingElse...]))
		
		An Action Request is fairly broad, and is used to request an action that may require
		some computation of the GameState.
	
	
	
	Entity Control Request:
		*** DEPRECATED IN FAVOUR OF ENTITY MOD REQUEST ***
		['EC', [58, changes] ] # EC flag for EntityControl. 58 is the EID of the entity we are attempting to contol.
		changes = { "P":[1.1, 5.6, 1.0] } # changing the position...
		
		Entity Control requests are used when a user wants to control variables of an entity.
		A good example if this would be a user controlling their player entity; they are not 
		the owner of the player entity, but they can use EC requests to control certain variables
		of the entity (like position and such).
	"""
	
	def __init__(self):
		print("  GameState's Request Handler ready.")
		pass
	
	def run(self, GameState, gpsnet):
		"""
		Grabs inbound packages from the gpsnet,
		handles them with handleRequest().
		"""
		items = gpsnet.inItems
		#print("\ninItems: %s\n"%(items))
		for item in items:
			sender, package = item
			packageFlag, request = package
			if packageFlag == 'GS':
				self.handleRequest(sender, request, GameState, gpsnet)
		#if items: print("\nGameState Changed!: %s\n"%(GameState.contents))
	
	
	
	
	def handleRequest(self, sender, request, GameState, gpsnet):
		"""
		Interprets a request to change the GameState.
		"""
		try:
			flag, data = request
			
			if flag == 'EC':
				# DEPRECATED, USE EM
				self.handleEntityControlRequest(data, sender, GameState, gpsnet)
			
			if flag == 'EM': # Entity Mod
				self.handleEntityModRequest(request, sender, GameState, gpsnet)
			
			if flag == 'VA': # Value Append
				self.handleValueAppendRequest(request, sender, GameState, gpsnet)
			
			if flag == 'AR': # Action Request
				self.handleActionRequest(request, sender, GameState, gpsnet)
		except:
			import traceback; traceback.print_exc()
	
	
	
	
	
	def handleEntityModRequest(self, request, sender, GameState, gpsnet):
		"""
		Handles an EM Request.
		"""
		flag, changes = request
		for change in changes:
			EID, type, key, value = change
			if key:
				GameState.contents['E'][EID][type][key] = value
			else:
				GameState.contents['E'][EID][type] = value
		GameState.changes.append(request)
	
	
	
	def handleValueAppendRequest(self, request, sender, GameState, gpsnet):
		"""
		Handles an VA Request.
		('VA', (1, 'CD', 'spawnRequestQueue', ['nanoshooter']))
		"""
		flag, data = request
		EID, type, key, valuesToAppend = data
		
		for value in valuesToAppend:
			GameState.contents['E'][EID][type][key].append(value)
		
		GameState.changes.append(request)
	
	
	
	
	def handleEntityControlRequest(self, data, sender, GameState, gpsnet):
		"""
		Handles an EC Request. DEPRECATED, USE ENTITY MOD REQUEST INSTEAD.
		"""
		EID = data[0]
		changes = data[1]
		
		for var in changes:
			value = changes[var]
			GameState.contents['E'][EID]['CD'][var] = value
		GameState.changes.append( ['EC', data] )
		
		# Getting the designated controlled UID for this entity
		# because only the designated controller is allowed to
		# perform an EC request.
		#controller = GameState.getEntity(EID)['C']
		
		#if sender == controller:
		#	# If the person sending this request is the controller of this entity,
		#	# then we'll do it.
		#	pass
		#else:
		#	# If the sender trying to do this is not the controller, then this isn't allowed...
		#	print("Error (Gamestate.RequestHandler, handleEntityControlRequest): Sender %s cannot control entity %s because they are not the designated controller for this entity; %s has control over this entity."%(sender, EID, controller))
	
	
	
	def handleActionRequest(self, request, sender, GameState, gpsnet):
		"""
		Handles an Action Request.
		"""
		flag, data = request
		actionFlag, actionData = data
		
		if actionFlag == "SE": # Spawn Entity...
			# ( entityType, (ownerID, controllerID), [arg_position, arg_rotation, arg_somethingElse...] )
			type, IDs, args = actionData
			ownerID, controllerID = IDs
			EID = GameState.addEntity(type, ownerID, controllerID, args)
			# We'll let this information be distributed in a full GS distro.
		
		if actionFlag == "RE": # Remove Entity
			EID = actionData
			GameState.removeEntity(EID)
			# We'll let this information be distributed in a full GS distro.
		
		if actionFlag == 'SP': # Spawn Player
			# DEPRECATED!!! #
			EID = GameState.addEntity('player')
			GameState.contents['E'][EID]['C'] = sender
			# We'll let this information be distributed in a full GS distro.
		
		if actionFlag == 'AU': # Add User
			name = actionData
			EID = GameState.addUser(sender)
			GameState.contents['U'][sender]['N'] = name
			# We'll let this information be distributed in a full GS distro.
		
	

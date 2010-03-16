### GameState.RequestHandler ###

class Class:
	"""
	Interprets requests to make changes to the GameState.
	GameState Request Protocol:
	
	Entity Control Request:
		* DEPRECATED IN FAVOUR OF ENTITY MOD REQUEST
		['EC', [58, changes] ] # EC flag for EntityControl. 58 is the EID of the entity we are attempting to contol.
		changes = { "P":[1.1, 5.6, 1.0] } # changing the position...
		
		Entity Control requests are used when a user wants to control variables of an entity.
		A good example if this would be a user controlling their player entity; they are not 
		the owner of the player entity, but they can use EC requests to control certain variables
		of the entity (like position and such).
	
	Entity Mod Request:
		['EM', changes]
		changes = [(change, change2, change3...)]
		change = (EID, type, key, value)
		change = (69, 'CD', 'position', [0.0, 0.0, 0.0])
	
	Value Append Request:
		['VA', EID, 'CD', 'someKindOfQueue', [valuesToAppend]]
	
	
	Action Request:
		['AR', action] # 'AR' flag obviously for ActionRequest.
		action = ['DMG', 52, 23] # this would be a request to apply 23 damage to player entity 52.
		action = ['SP', 69, 12] #DEPRECATED!USE-BELOW! This would spawn a player entity with control given to UID 69.
		action = ['SE', 'nanoshooter'] # Spawns an entity, the sender of the message gets control, the host gets ownership.
		
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
		items = gpsnet.inItems
		#print("\ninItems: %s\n"%(items))
		for item in items:
			sender = item[0]
			package = item[1]
			packageFlag = package[0]
			request = package[1]
			if packageFlag == 'GS':
				self.handleRequest(sender, request, GameState, gpsnet)
		#if items: print("\nGameState Changed!: %s\n"%(GameState.contents))
	
	
	
	
	def handleRequest(self, sender, request, GameState, gpsnet):
		"""
		Interprets a request to change the GameState.
		"""
		try:
			flag = request[0]
			data = request[1]
			
			if flag == 'EC':
				# DEPRECATED, USE EM
				self.handleEntityControlRequest(data, sender, GameState, gpsnet)
			
			if flag == 'EM': # Entity Mod
				self.handleEntityModRequest(request, sender, GameState, gpsnet)
			
			if flag == 'VA': # Value Append
				self.handleValueAppendRequest(request, sender, GameState, gpsnet)
			
			if flag == 'AR':
				self.handleActionRequest(data, sender, GameState, gpsnet)
		except:
			import traceback; traceback.print_exc()
	
	
	
	
	
	def handleEntityModRequest(self, request, sender, GameState, gpsnet):
		"""
		Handles an EM Request.
		"""
		flag = request[0]
		changes = request[1]
		for change in changes:
			EID=change[0]
			type=change[1]
			key=change[2]
			value=change[3]
			if key:
				GameState.contents['E'][EID][type][key] = value
			else:
				GameState.contents['E'][EID][type] = value
		GameState.changes.append(request)
	
	
	
	def handleValueAppendRequest(self, request, sender, GameState, gpsnet):
		"""
		Handles an VA Request.
		['VA', EID, 'CD', 'someKindOfQueue', [valuesToAppend]]
		"""
		flag = request[0]
		EID = request[1]
		type = request[2]
		key = request[3]
		valuesToAppend = request[4]
		
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
	
	
	
	def handleActionRequest(self, action, sender, GameState, gpsnet):
		"""
		Handles an Action Request.
		"""
		flag = action[0]
		
		if flag == "SE": # Spawn Entity...
			type = action[1]
			EID = GameState.addEntity(type, GameState.Admin.getUID(), sender) # We are the Owner, sender is the controller.
			# We'll let this information be distributed in a full GS distro.
		
		if flag == "RE": # Remove Entity
			EID = action[1]
			GameState.removeEntity(EID)
			# We'll let this information be distributed in a full GS distro.
		
		if flag == 'SP': # Spawn Player
			# DEPRECATED!!! #
			EID = GameState.addEntity('player')
			GameState.contents['E'][EID]['C'] = sender
			# We'll let this information be distributed in a full GS distro.
		
		if flag == 'AU': # Add User
			name = action[1]
			EID = GameState.addUser(sender)
			GameState.contents['U'][sender]['N'] = name
			# We'll let this information be distributed in a full GS distro.
		
	

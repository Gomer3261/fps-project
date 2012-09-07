class initializeGamestate:
	"""
	Gamestate is a class designed to manage game related data that is transferred over a network.
	The class is intended to hold specific user, entity, and game related data, as well as handling changesets
	allowing class users to submit and merge changes from multiple sources.
	"""
	def __init__(self):
		import engine
		self.engine = engine
		
		self.delta = {}
		self.clear()
		
		self.nextId = 1
	
	
	
	#-----------------------#
	#-- Editing Gamestate --#
	#-----------------------#
	
	def getNextId(self):
		"""
		Usage: getNextId()
			returns the next unused id for the gamestate, only the host gamestate can produce unique ids.
		Returns: a unique id for storage in the gamestate.
		"""
		id = self.nextId
		self.nextId += 1
		return id
	
	def deleteNullities(self, dict1, dict2):
		"""
		Usage: deleteNullities(dict1, dict2)
			deletes null values from the dictionary tree dict1 from dict1 and dict2.
		dict1: The dictionary containing null values to remove from both dictionarys.
		dict2: The dictionary to remove values from.
		Returns: Nothing.
		"""
		list = []
		for i in dict1:
			if i in dict2 and type(dict1[i]) == type({}):
					self.deleteNullities(dict1[i], dict2[i])
			elif dict1[i] == None:
				list.append(i)
		for i in list:
			del dict1[i]
			if i in dict2:
				del dict2[i]
				
	def updateRecursively(self, value1, value2):
		"""
		Usage: updateRecursivelt(value1, value2)
			Merges two dictionary trees, the second value into the first value.
		value1: The dictionary to merge value2 into.
		value2: The dictionary to be merged into value 1.
		Returns: The resulting merged dictionary.
		"""
		for i in value2:
			if i in value1 and (type(value1[i]) == type({})) and (type(value2[i]) == type({})):
				value1[i] = self.updateRecursively(value1[i], value2[i])
			else:
				value1[i] = value2[i]
		return value1
		
	def scanDelta(self):
		"""
		Usage: scanDelta()
			Scans the gamestate's saved delta and removes incorrect changes.
		Returns: None
		"""
		if 'E' in self.delta:
			toDelete=[]
			for id in self.delta['E']:
				if not 't' in self.delta['E'][id]: toDelete.append(id)
			for id in toDelete: del self.delta['E'][id]
				
	def applyDelta(self):
		"""
		Usage: applyDelta()
			Merges the gamestate's saved delta into the gamestate itself.
		Returns: None
		"""
		self.deleteNullities(self.delta, self.data)
		self.updateRecursively(self.data, self.delta)
		
	def mergeDelta(self, deltaData):
		"""
		Usage: mergeDelta(deltaData)
			Merges a piece of delta data into the gamestate's saved delta.
		deltaData: Dictionary delta to merge into the gamestate's saved delta.
		Returns: None
		"""
		#TODO: Possiblity of loss in null values. Proper Nullity handling may be necessary.
		self.scanDelta()
		self.delta = self.updateRecursively(self.delta, deltaData)
	
	def addUser(self, username):
		"""
		Usage: addUser(username)
			Adds a new user to the gamestate.
		username: String name to give the new user.
		Returns: The id of the new user. None if failure occurs.
		"""
		if self.engine.host:
			newId = self.getNextId()
			self.mergeDelta( {'U':{newId:{'n':username}}} )
			return newId
		else:
			print("Gamestate error: client gamestate cannot produce unique object id. No user was created.")
			return None
		
	def removeUser(self, id):
		"""
		Usage: removeUser(id)
			Removes a user from the gamestate.
		id: Integer id to remove from users.
		Returns: None
		"""
		if self.engine.host:
			self.mergeDelta( {'U':{id:None}} )
		else:
			print("Gamestate error: client gamestate cannot remove users. No action was taken.")
						
	def addEntity(self, type, controller=None):
		"""
		Usage: addEntity(type, controller=None)
			Adds an entity of the given type, with the given controller to the gamestate.
		type: String type of the entity being added.
		controller: Integer id of the controller of the new entity. If None, the current engine is used as the controller.
		Returns: The id of the new entity. None if failure occurs.
		"""
		if controller == None:
			controller = self.engine.id
		if self.engine.host:
			if self.containsUser(controller):
				newId = self.getNextId()
				self.mergeDelta( {'E':{newId:{'t':type,'c':controller}}} )
				return newId
			else:
				print("Gamestate error: specified controller: " + str(controller) + " does not exist in the gamestate. No entity was created.")
		else:
			print("Gamestate error: client gamestate cannot produce unique object id. No entity was created.")
		return None
			
	def removeEntity(self, id):
		"""
		Usage: removeEntity(id)
			Deletes an entity from the gamestate.
		id: Integer id to delete.
		Returns: None
		"""
		self.mergeDelta( {'E':{id:None}} ) #TODO: Anyone can remove entities.
		#if self.engine.host:
		#	self.mergeDelta( {'E':{id:None}} )
		#else:
		#	print("Gamestate error: client gamestate cannot remove entities. No action was taken.")
	
	
	
	#-----------------------#
	#-- Reading Gamestate --#
	#-----------------------#
	
	def getById(self, id):
		"""
		Usage: getById(id)
			Used to obtain the data of a specified id from the gamestate.
		id: Integer id to search for.
		Returns: The data stored in the gamestate under the specified id. None if the id does not exist.
		"""
		if id in self.data['U']:
			return self.data['U'][id]
		elif id in self.data['E']:
			return self.data['E'][id]
		else:
			return None
			
	def hasEntity(self, userid, type):
		"""
		Usage: hasEntity(userId, type)
			Checks if a specified user has control of an instance of a certain entity type.
		userid: Integer id of the user to check for.
		type: String type of the entity type to check for.
		Returns: True if the user controls an entity of the specified type.
		"""
		if self.containsUser(userid):
			for i in self.data['E']:
				if self.data['E'][i]['c'] == userid and self.data['E'][i]['t'] == type:
					return True
		return False;
		
	def containsUser(self, id):
		"""
		Usage: containsUser(userId)
			Determines if an id exists in the gamestate's user dictionary.
		id: Integer id to search for.
		Returns: True if the id exists in the gamestate's users.
		"""
		if (id in self.data['U']):
			return True
		return False
	
	def containsEntity(self, id):
		"""
		Usage: containsEntity(entityId)
			Determines if an id exists in the gamestate's entity dictionary.
		id: Integer id to search for.
		Returns: True if the id exists in the gamestate's entities.
		"""
		if (id in self.data['E']):
			return True
		return False
		
	def containsId(self, id):
		"""
		Usage: containsId(id)
			Determines if an id exists in the gamestate as a user or entity.
		id: Integer id to search for.
		Returns: True if the id exists in the gamestate.
		"""
		if (self.containsUser(id)) or (self.containsEntity(id)):
			return True
		return False
	
	def hasControl(self, id):
		#TODO: This function checks engine id, instead of the users id. Look further into it.
		"""
		Usage: hasControl(entityId)
			Checks if the current
		id: Integer id to search for.
		Returns: Integer id of the entitie's controller, None if the entity does not exist.
		"""
		if(self.containsEntity(id)):
			entity = self.data['E'][id]
			return (entity['c']==self.engine.id)
		return None
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	#---------------------------#
	#-- Gamestate Data Access --# (eliminating gamestate.data from outside view) kind of wish I had private values :(
	#---------------------------#
			
	def keys(self):
		return self.data.keys()
	
	def values(self):
		return self.data.values()
		
	def items(self):
		return self.data.items()
		
	def get(self, key, default=None):
		return self.data.get(key, default)
		
	def clear(self):
		self.data = {}
		self.data["U"] = {}
		self.data["E"] = {}
		self.data["G"] = {}
		self.delta.clear()
		
	def setdefault(self, key, default=None):
		self.data.setdefault(key, default)
		
	def pop(self, key, default=None):
		return self.data.pop(key, default)
		
	def popitem(self):
		return self.data.popitem()
		
	def copy(self):
		return self.data.copy()
		
	def update(self, dict):
		return self.data.update(dict)
		
	def __len__(self):
		return len(self.data)
		
	def __getitem__(self, key):
		return self.data[key]
		
	def __setitem__(self, key, value):
		self.data[key] = value
		
	def __delitem__(self, key):
		del self.data[key]
		
	def __iter__(self):
		return self.data.__iter__()
		
	def __contains__(self, key):
		return key in self.data
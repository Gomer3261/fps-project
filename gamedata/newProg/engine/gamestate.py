class initializeGamestate:
	def __init__(self):
		import engine
		self.engine = engine
		
		self.delta = {}
		self.clear()
		
		self.nextId = 1
		
	#Managerial functions
	
	def getNextId(self):
		id = self.nextId
		self.nextId += 1
		return id
	
	#Editing gamestate
	
	def deleteNullities(self, dict1, dict2):
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
		for i in value2:
			if i in value1 and (type(value1[i]) == type({})) and (type(value2[i]) == type({})):
				value1[i] = self.updateRecursively(value1[i], value2[i])
			else:
				value1[i] = value2[i]
		return value1
		
	def scanDelta(self):
		if 'E' in self.delta:
			toDelete=[]
			for id in self.delta['E']:
				if not 't' in self.delta['E'][id]: toDelete.append(id)
			for id in toDelete: del self.delta['E'][id]
				
	def applyDelta(self):
		self.deleteNullities(self.delta, self.data)
		self.updateRecursively(self.data, self.delta)
		
	def mergeDelta(self, deltaData):
		#Possiblity of loss in null values. Propery Nullity handling may be necessary
		self.scanDelta()
		self.delta = self.updateRecursively(self.delta, deltaData)
	
	def addUser(self, username):
		if self.engine.host:
			newId = self.getNextId()
			self.mergeDelta( {'U':{newId:{'n':username}}} )
			return newId
		else:
			print("Gamestate error: client gamestate cannot produce unique object id. No user was created.")
		
	def removeUser(self, id):
		if self.engine.host:
			self.mergeDelta( {'U':{id:None}} )
		else:
			print("Gamestate error: client gamestate cannot remove users. No action was taken.")
						
	def addEntity(self, type, controller=None):
		if controller == None:
			controller = self.engine.id
		if self.engine.host:
			newId = self.getNextId()
			self.mergeDelta( {'E':{newId:{'t':type,'c':controller}}} )
			return newId
		else:
			print("Gamestate error: client gamestate cannot produce unique object id. No entity was created.")
			
	def removeEntity(self, id):
		self.mergeDelta( {'E':{id:None}} ) # Anyone can remove entities.
		#if self.engine.host:
		#	self.mergeDelta( {'E':{id:None}} )
		#else:
		#	print("Gamestate error: client gamestate cannot remove entities. No action was taken.")
	
	
	#Reading Gamestate
		
	def getById(self, id):
		if id in self.data['U']:
			return self.data['U'][id]
		elif id in self.data['E']:
			return self.data['E'][id]
		else:
			return None
	
	def hasControl(self, id):
		entity = self.data['E'][id]
		return (entity['c']==self.engine.id)
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	#Don't look at it!
		
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
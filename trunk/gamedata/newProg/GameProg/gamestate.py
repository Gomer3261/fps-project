class GAMESTATE:
	def __init__(self, net, host)
		self.data = {}
		self.delta = {}
		
		self.net = net
		self.host = host
		self.mode = None
	
	#Editing gamestate
	
	def deleteNullities(self, dict1, dict2)
		list = []
		for i in dict1:
			if dict1[i] == None:
				list.append(i)
			elif isinstance(dict1[i], dict)
				self.deleteNullities(dict1[i], dict2[i])
		for i in list:
			del dict1[i]
			try:
				del dict2[i]
			except:
				continue
				
	def updateRecursively(self, value1, value2)
		for i in value2:
			if isinstance(value1[i], dict) and isinstance(value2[i], dict):
				self.recursiveUpdate(value1[i], value2[i])
			else:
				value1[i] = value2[i]
				
	def applyDelta(self)
		self.deleteNullities(self.delta, self.data)
		self.updateRecursively(self.data, self.delta)
		
	def mergeDelta(self, deltaData)
		#Possiblity of loss in null values. Propery Nullity handling may be necessary
		self.updateRecursively(self.delta, deltaData)
	
	def interpret(self, buffer)
		#Do stuff!
	
	
	
	
	#Reading Gamestate
	
	def addUsers(self, newUsers)
		#Do stuff!
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	#Don't look at it!
		
	def keys(self)
		return self.data.keys()
	
	def values(self)
		return self.data.values()
		
	def items(self)
		return self.data.items()
		
	def get(self, key, default=None)
		return self.data.get(key, default)
		
	def clear(self)
		self.data.clear()
		
	def setdefault(self, key, default=None)
		self.data.setdefault(key, default)
		
	def pop(self, key, default=None)
		return self.data.pop(key, default)
		
	def popitem(self)
		return self.data.popitem()
		
	def copy(self)
		return self.data.copy()
		
	def update(self, dict)
		return self.data.update(dict)
		
	def __len__(self)
		return len(self.data)
		
	def __getitem__(self, key)
		return self.data[key]
		
	def __setitem__(self, key, value)
		self.data[key] = value
		
	def __delitem__(self, key)
		del self.data[key]
		
	def __iter__(self)
		return self.data.__iter__()
		
	def __contains__(self, key)
		return key in self.data
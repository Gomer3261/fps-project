# Entities

class Class:
	def __init__(self, id, gamestate, entityController):
		self.id = id
		self.entityController = entitiyController
		self.initiate( gamestate )
		
	def initiate(self, data):
		pass
		#Create game objects and such here. Remember to you import bge
		
	def end():
		pass
		#Remove game objects and handle any deconstruction methods/issues
		
	def run( gamestate ):
		pass
		#Regular controller rountine, use for movement, and such. Only run by controlling computer
		
	def conform( gamestate ):
		if gamestate["E"][id]["control"]:
			pass
			#Run controller replication
		else:
			pass
			#Run proxy replication
		
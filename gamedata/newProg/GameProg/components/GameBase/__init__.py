### GameBase Component ###
# GameBase.Class
class Class:
	def __init__(self, cont):
		# Instancing the camera subcomponent
		import camera
		self.camera = camera.Class(cont)
	
	def run(self, Interface, GameControl):
		# Running the camera subcomponent
		self.camera.run(Interface.options, GameControl.localGame)

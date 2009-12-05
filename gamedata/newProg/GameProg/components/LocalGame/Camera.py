class Class:
	"""
	Cameras.
	Camera Game Objects must have a property named "priority". Cameras will
	compete for activity by repeatedly using the set() function here, and the
	camara with the highest priority is chosen.
	"""
	
	def __init__(self):
		# Spawning the eCam (Emergency Camera)
		import GameLogic as gl
		own = gl.getCurrentController().owner
		self.eCam = gl.getCurrentScene().addObject("eCam", own)
		gl.getCurrentScene().active_camera = self.eCam
	
	def set(self, cam=None):
		import GameLogic as gl
		scene = gl.getCurrentScene()
		
		# If no cam is specified, we use the emergencyCamera.
		if not cam:
			cam = self.eCam
		
		# If scene.active_camera != cam
		if scene.active_camera != cam:
			if not "priority" in cam:
				cam["priority"] = 0
			
			if "priority" not in scene.active_camera:
				scene.active_camera["priority"] = -1
			
			if cam['priority'] > scene.active_camera['priority']:
				scene.active_camera = cam
				print("New Camera Set!")
	
	def forceSet(self, cam=None):
		import GameLogic as gl
		scene = gl.getCurrentScene()
		if not cam:
			cam = self.eCam

		# If cam, we will replace the active_camera, but only if cam has greater priority.
		if not "priority" in cam:
			cam["priority"] = 0
		
		scene.active_camera = cam
	
	def clear(self):
		import GameLogic as gl
		scene = gl.getCurrentScene()
		cam = self.eCam
		scene.active_camera = cam

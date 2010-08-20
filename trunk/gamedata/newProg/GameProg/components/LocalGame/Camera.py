class Class:
	"""
	Cameras.
	Camera Game Objects must have a property named "priority". Cameras will
	compete for activity by repeatedly using the set() function here, and the
	camara with the highest priority is chosen.
	"""
	
	def __init__(self):
		# Spawning the eCam (Emergency Camera)
		import bge
		own = bge.logic.getCurrentController().owner
		self.eCam = bge.logic.getCurrentScene().addObject("eCam", own)
		self.eCam.position = [0.0, 0.0, 50.0]
		bge.logic.getCurrentScene().active_camera = self.eCam
		print("  Camera's happy.")
	
	def set(self, cam=None):
		import bge
		scene = bge.logic.getCurrentScene()
		
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
		import bge
		scene = bge.logic.getCurrentScene()
		if not cam:
			cam = self.eCam

		# If cam, we will replace the active_camera, but only if cam has greater priority.
		if not "priority" in cam:
			cam["priority"] = 0
		
		scene.active_camera = cam
	
	def clear(self):
		import bge
		scene = bge.logic.getCurrentScene()
		cam = self.eCam
		scene.active_camera = cam

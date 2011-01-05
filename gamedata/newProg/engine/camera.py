### Camera System ###

import bge
scene = bge.logic.getCurrentScene()

eCam = scene.objects['eCam']
scene.active_camera = eCam
currentCameraPriority = 0

# Every camera will call this each tick, and they will fight for supremacy
def offer(camera, priority):
	global scene, eCam, currentCameraPriority
	if camera != scene.active_camera:
		if priority > currentCameraPriority:
			scene.active_camera = camera
			currentCameraPriority = priority

def reset():
	global scene, eCam, currentCameraPriority
	scene.active_camera = eCam
	currentCameraPriority = 0

def resetPriority():
	global currentCameraPriority
	currentCameraPriority = 0
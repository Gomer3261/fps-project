### ############################### ###
### ### ------ gametools ------ ### ###
### ############################### ###
### # The FPS Project
INIT = 1

def interpolatePosition(start, target, speed):
	"""
	Super simple method of smoothing the transition from point A to B.
	Calling this function returns a position between the two points based on speed.
	Speed should be between 0.0 and 1.0.
	"""
	# Difference of start to target.
	dX = target[0] - start[0]
	dY = target[1] - start[1]
	dZ = target[2] - start[2]
	
	# The offset to be applied to the start position
	oX = dX * speed
	oY = dY * speed
	oZ = dZ * speed
	
	# Getting the new position
	X = start[0] + oX
	Y = start[1] + oY
	Z = start[2] + oZ
	
	return [X, Y, Z]

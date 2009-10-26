# The FX System.
spawnerObj = None
scene = None
### Initiates the scene and spawner object. The scene thing doesn't seem to work.
# Will probably just use GameLogic.getCurrentScene instead of doing the scene initiation.
def init(con):
	global spawnerObj
	global scene
	spawnerObj = con.owner
	import GameLogic
	scene = GameLogic.getCurrentScene()
	print "FX Initiated."



### Instantly spawns an effect.
def spawn(effect="FX_cubeSplode", vars={}):
	global spawnerObj
	global scene
	
	if spawnerObj and scene:
		obj = scene.addObject(effect, spawnerObj)
		obj.position = [0.0, 0.0, 10.0]
		for prop in vars:
			value = vars[prop]
			obj[prop] = value
		return obj
	else:
		print "ERROR: FX System not initialized."



### For spawning objects into the correct scene from another scene by 
# queuing them up and spawning them in another pass (maybe the next frame).
requests = []
def handleRequests(con):
	global requests
	for request in requests:
		effect, vars = request
		spawn(effect, vars)
	requests = []
def request(effect="FX_cubeSplode", vars={}):
	global requests
	requests.append( (effect, vars) )







############################################################################
######============------      EFFECT FUNCTIONS      ------============######
############################################################################

def cubeSplode(con):
	"""
	The programming for the cubeSplode effect.
	"""

	global scene
	global spawnerObj
	
	obj = con.owner
	subParticleName = "FX_cubeSplode-cube"
	
	import random
	
	for i in range(obj["num"]):
		life = int(randomize(obj["life"], obj["lifeRand"]))
		subParticle = scene.addObject(subParticleName, spawnerObj, life) # For 10 Frames
		
		subParticle.position = obj.position
		subParticle.localScale = [obj["size"], obj["size"], obj["size"]]
		
		randomVector = makeRandomVector()
		subParticle["X"] = (randomVector[0] * obj["speed"] / 10) * obj["size"]
		subParticle["Y"] = (randomVector[1] * obj["speed"] / 10) * obj["size"]
		subParticle["Z"] = (randomVector[2] * obj["speed"] / 10) * obj["size"]
	
	obj.endObject()

def cubeSplodeSub(con):
	"""
	The programming for the cubeSplode effect's subparticles.
	"""
	obj = con.owner
	obj.applyMovement([obj["X"], obj["Y"], obj["Z"]], 0)















######################################################################################################
######============------      Various Multipurpose Functions For Effects      ------============######
######################################################################################################

def makeRandomVector():
	result = []
	import random
	for i in range(3):
		value = random.random()
		negate = random.choice([True, False])
		if negate:
			value *= -1
		result.append(value)
	return result

def randomize(base, rand):
	"""
	Primarily made for use with floats...
	"""
	base = float(base)
	rand = float(rand)
	import random
	rand = rand * random.random()
	negate = random.choice([True, False])
	if negate:
		rand *= -1
	return base+rand

### ####################################### ###
### ### ------ BALLISTICS ENGINE ------ ### ###
### ####################################### ###
### # The FPS Project
INIT = 0
manager = None # initiated at bottom

def dependenciesAreHappy():
	import modules
	return (modules.timetools)

def init(con):
	global INIT
	global manager, MANAGER
	manager = MANAGER(con)
	INIT = 1
	print "Ballistics Initiated"

def initLoop(con):
	global INIT

	if dependenciesAreHappy() and (not INIT):
		init(con)
	else:
		pass








class MANAGER:
	"""
	The Ballistics Manager.
	It handles the simulation of every bullet projectile in the game.
	"""

	import modules

	def __init__(self, con):
		self.raycaster = con.owner # The object that is used for raycasting.
		self.bulletTypes = self.modules.classes.bulletTypes # I don't think this is actually ever used... Remove?
		self.timetools = self.modules.timetools # Hmm...

	pool = [] # Pool of bullets to be simulated.
	deadPool = [] # List of bullets that need to be removed from the pool; they're dead.

	def addToSimulation(self, bullet):
		"""
		Adds a bullet object to the ballistics simulation.
		"""
		# Timer for ballistics simulation. Giving it a 1 frame headstart.
		# =OPTIMIZE=: Perhaps it's dumb to give each individual bullet it's own timer? But useful if we break the simulation up into multiple passes... hmmm... Give each pass a timer instead?
		bullet.timer = self.timetools.TIMER(self.modules.timetools.perFrame())
		
		# Starting the bullet.path at the bullet's starting point (this path thing probably shouldn't be used; it seems like something that would lag things out.
		bullet.path.append(bullet.position)

		# Adding it to the simulation pool
		self.pool.append(bullet)
	
	
	
	def debugBullets(self):
		"""
		Just prints out some debug information about each bullet in the pool.
		"""
		print "\n\nBullet Info:"
		for bullet in self.pool:
			print "    - bullet position=%s, direction=%s" % (bullet.position, bullet.direction)
	
	
	def terminateBullet(self, bullet):
		"""
		Marks a bullet for deletion.
		"""
		self.deadPool.append(bullet)
	
	def doBulletImpact(self, bullet):
		pass
	
	







	def run(self):
		# Hehe...
		self.runSimulation()
	
	### ================================================
	### Simulation
	### ================================================

	def runSimulation(self):
		"""
		Performs ballistics simulation for each bullet.
		Can divide the bullet pool into multiple passes for simulation
		to divide up the workload (while decreasing authenticity of the
		simulation).
		"""
		for bullet in self.pool:
			# The actual simulation for each bullet
			self.bulletSim(bullet)
		self.cleanThePool()

	def cleanThePool(self):
		for deadBullet in self.deadPool:
			self.pool.remove(deadBullet)
		self.deadPool = []


	### ================================================
	### The Actual Simulation (for real this time)
	### ================================================

	def bulletSim(self, bullet):
		"""
		The external simulation of a single bullet.
		"""
		debug = 1
		
		# Getting the length of time that this simulation step is simulating.
		stepTime = bullet.timer.get() / 100
		bullet.timer.reset()
		
		# Let's pretend we're actually factoring in cool stuff for now...
		self.factorDamping(bullet, stepTime)
		self.factorGravity(bullet, stepTime)
		self.factorRandomness(bullet, stepTime)
		
		# Recording the last position before projection (so we can Rasterizer.drawLines() :)
		lastPosition = bullet.position
		
		# Projecting the bullet... (which also will move the bullet's position...)
		hit, point, normal = self.projectBullet(bullet, stepTime)
		if hit:
			# If the bullet hits anything, then we'll factor the impact for fun.
			self.factorImpact(bullet, hit, point, normal, stepTime)
		
		# Okay, now it's time to draw pretty lines..
		if debug:
			d1 = lastPosition
			d2 = bullet.position
			import Rasterizer
			Rasterizer.drawLine(d1, d2, [1.0, 0.0, 0.0])
		
		# This chunk makes it so that the bullet is deleted after it has been hanging around for too long.
		bullet.step += 1
		if bullet.step >= bullet.maxsteps:
			# Bullet has run out of simulation time; killing bullet
			self.terminateBullet(bullet)




	def factorDamping(self, bullet, stepTime):
		"""
		Simulates the affects of air friction and things 
		related to that on the bullet.
		Includes velocity loss and stability loss.
		"""
		return None

	def factorGravity(self, bullet, stepTime):
		"""
		Simulates the affects of gravity on the bullet.
		"""
		return None

	def factorRandomness(self, bullet, stepTime):
		"""
		Simulates the randomization of certain factors.
		For example, bullet direction is randomely affected
		based on the bullets stability (or lack thereof).
		"""
		return None




	def projectBullet(self, bullet, stepTime):
		"""
		Projects a ray from current position to the next position.
		If the raycast doesn't hit anything, the bullet is moved to
		the new position.
		This method returns (hit, point, normal) from the raycast results.
		"""
		# Using stepTime to get the displacement magnitude for this step.
		M = bullet.velocity * stepTime # Positional displacement Magnitude.
		D = self.normalize(bullet.direction) # 3D Direction Vector
		
		# Getting the local offset for movement.
		X = D[0] * M
		Y = D[1] * M
		Z = D[2] * M
		offset = [X, Y, Z]
		
		# Globalizing said local offset...
		newPosition = self.offset(bullet.position, offset)
		
		# rayCast(objto, objfrom, dist, prop, face, xray, poly)
		hit, point, normal = self.raycaster.rayCast(bullet.position, newPosition, 0, "ballistics", 0, 1, 0) # Raycasting...

		if hit: # If the bullet hit something...
			bullet.position = point

			# Saving the hit data to the bullet
			bullet.hit = hit
			bullet.point = point
			bullet.normal = normal

		else:
			# The bullet didn't hit anything, so we can safely
			# move the bullet to the newPosition.
			bullet.position = newPosition

		# Adding the new position to the path (used for drawing the bullet)
		# =OPTIMIZE=: Perhaps recording the path of a bullet is a performance issue?
		#bullet.path.append(newPosition)
		# ^ Yeah, lets not do that; sounds laggey if you ask me man...
				
		return hit, point, normal
	
	
	def factorImpact(self, bullet, hit, normal, point, stepTime):
		"""
		It's supposed to factor an impact and decide if the bullet should be terminated,
		perhaps along with a fancy bullet impact effect, or perhaps it should penetrate and keep
		on going, or even deflect... This will be a fun method.
		"""
		self.doBulletImpact(bullet)
		self.terminateBullet(bullet)
			









	### ================================================
	### General Purpose Methods
	### ================================================

	def normalize(self, v):
		"""
		Normalizes a 3D vector.
		"""
		x = v[0]
		y = v[1]
		z = v[2]

		import math
		length = math.sqrt( (x*x + y*y + z*z) )

		X = x/length
		Y = y/length
		Z = z/length

		return [X, Y, Z]

	def offset(self, pos, off):
		pX = pos[0]
		pY = pos[1]
		pZ = pos[2]

		oX = off[0]
		oY = off[1]
		oZ = off[2]

		X = pX + oX
		Y = pY + oY
		Z = pZ + oZ

		return [X, Y, Z]


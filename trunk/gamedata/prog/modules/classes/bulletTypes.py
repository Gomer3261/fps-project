### #################################### ###
### ### ------ BULLET CLASSES ------ ### ###
### #################################### ###
### # The FPS Project
INIT = 1


class BULLET:
	"""
	This is the default bullet class.
	It is used both for inventory information,
	and for ballistics information.
	"""

	
	### ================================================
	### UNIVERSAL DATA
	### ================================================
	name = "STA"
	diameter = 6.0 # in millimeters
	mass = 6.0 # in grams
	regularVelocity = 925.0 # in meters per second
	
	type = "fmj" # Full Metal Jacket
	# Other types include:
	# blank
	# tracer
	# explosive
	# peircing
	# hollow
	
	### ================================================
	### ITEM DATA
	### ================================================
	description = "Standard Assault Round"
	cost = 1.0 # in dollars
	weight = (mass*3.0) / 1000.0 # Of entire cartridge, in kilograms. Mass is tripled because mass is just for the bullet.

	### ================================================
	### BALLISTICS CONSTANTS
	### ================================================
	maxsteps = 200 # Maximum external ballistics simulation steps.
	owner = None # Gameblender object for raycasting
	timer = None # Timer for ballistics simulation

	### ================================================
	### BALLISTICS VARIABLES
	### ================================================
	owner = None # The ticket of the owner player.

	### Basic Variables ###
	step = 0
	path = []
	gravity = 0.0 # downwards velocity (meters per second)
	
	### Set by Internal Ballistics (in weapon simulator) ###
	position = [0.0, 0.0, 0.0] # Current position of the bullet in global coordinates
	direction = [0.0, 1.0, 0.0] # Normalized Directional Vector.
	velocity = regularVelocity # copied from regularVelocity
	stability = 1.0 # 1.0 = 100% perfect bullet trajectory, 0.0 = miserable failure of bullet trajectory

	### Terminal Ballistics Attributes (set by external ballistics before being sent to terminal) ###
	hit = None
	point = None
	normal = None

	### ================================================
	### BASIC CALCULATIONS
	### ================================================
	power = 0.0 # Kinetic Energy (in Joules)
	momentum = 0.0 # Mass * Velocity
	drag = 0.0 # Projectile drag in made up units.
	damage = 0.0 # Damage from chest shot in player health
	
	### ================================================
	### GUN SIMULATION DATA
	### ================================================
	fired = 0




	def calculate(self):
		self.power = ((self.mass/1000.0) * (self.velocity**2)) / 2.0 # E = MV^2/2, mass converted into kilograms
		self.momentum = self.mass/1000.0 * self.velocity # MV, mass converted into kilograms
		self.drag = self.diameter**2 / self.mass

		# Damage Formula (at muzzle velocity, hit in chest)
		self.damage = ((self.diameter**2) * self.power/1000.0)
		self.damage *= 0.25 # Weakening the damage for gameplay reasons. 1.0 for Hardcore mode, 0.25 for Normal mode, and 0.1 for Arcade mode.



# A Dictionary of bullet classes by bullet name.
bullets = {}

# PTL (Pistol Round)
class PTL(BULLET):
	name = "PTL"
	description = "Pistol Round"
	cost = 0.5
	
	diameter = 12.0
	mass = 12.0
	regularVelocity = 330.0
bullets["PTL"] = PTL

# STA (Standard Assault Round)
class STA(BULLET):
	name = "STA"
	description = "Standard Assault Round"
	cost = 1.0
	
	diameter = 6.0
	mass = 6.0
	regularVelocity = 925.0
bullets["STA"] = STA

# DMR (Designated Marksman Round)
class DMR(BULLET):
	name = "DMR"
	description = "Designated Marksman Round"
	cost = 1.5
	
	diameter = 8.0
	mass = 12.0
	regularVelocity = 800.0
bullets["DMR"] = DMR

# AMR (Anti-Material Round)
class AMR(BULLET):
	name = "AMR"
	description = "Anti-Material Round"
	cost = 3.0
	
	diameter = 14.0
	mass = 45.0
	regularVelocity = 800.0
bullets["AMR"] = AMR






### ================================================
### DEBUG/DEVELOPMENTAL STUFF LURKS BELOW!
### ================================================

def calcChestShots(dmg):
	a = 100.0 / dmg
	b = round(a, 0)
	if a != b:
		return int(a) + 1
	else:
		return int(a)

def calcLimbShots(dmg):
	a = 100.0 / (dmg*0.25)
	b = round(a, 0)
	if a != b:
		return int(a) + 1
	else:
		return int(a)


def printBullets():
	for bullet in bullets:
		B = bullets[bullet]()
		B.calculate()
		print "%s:" % (bullet)
		print "  Constants:"
		print "    Diameter: %s mm" % (B.diameter)
		print "    Mass: %s grams" % (B.mass)
		print "    Velocity: %s m/s" % (B.regularVelocity)
		print "  Calculated (at muzzle velocity):"
		print "    Drag: %.1f" % (B.drag)
		print "    Power: %.1f kJ" % (B.power/1000.0)
		print "    Recoil/Momentum: %.1f" % (B.momentum)
		print "    Damage: %.1f (kill: %s chest shots, %s limb shots, 1 headshot)\n\n" % (B.damage, calcChestShots(B.damage), calcLimbShots(B.damage))

#printBullets()

	

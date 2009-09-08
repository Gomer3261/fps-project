################################
### ------ ballistics ------ ###
################################
### Copyright 2009 Chase Moskal
INIT = 0


class BULLET:
    diamter = 0.0 # in millimeters
    mass = 0.0 # in grams
    velocity = 0.0 # in meters per second
    instability = 0.0 # in made up units
    gravity = 9.8 # in meters per second per second (acceleration)
    terminalvelocity = 98.0 # in meters per second

    power = 0.0 # Kinetic Energy (in Joules)
    momentum = 0.0 # Mass * Velocity
    drag = 0.0 # Projectile drag in made up units.
    damage = 0.0 # Damage from chest shot in player health

    def __init__(self, diameter=6.0, mass=6.0, velocity=925.0, gravity=9.8, terminalvelocity=98.0):
        self.diameter = diameter
        self.mass = mass
        self.velocity = velocity
        self.gravity = gravity
        self.terminalvelocity = terminalvelocity

    def calculate(self):
        self.power = ((self.mass/1000.0) * (self.velocity**2)) / 2.0 # E = MV^2/2, mass converted into kilograms
        self.momentum = self.mass/1000.0 * self.velocity # MV, mass converted into kilograms
        self.drag = self.diameter**2 / self.mass

        # Damage Formula (at muzzle velocity, hit in chest)
        self.damage = ((self.diameter**2) * self.power/1000.0)
        self.damage *= 0.25 # Weakening the damage for gameplay reasons. 1.0 for Hardcore mode, 0.25 for Normal mode, and 0.1 for Arcade mode.




bullets = {}

# PTL (Pistol Round)
PTL = BULLET()
PTL.diameter = 12.0
PTL.mass = 12.0
PTL.velocity = 330.0
PTL.calculate()
bullets["PTL"] = PTL

# STA (Standard Assault Round)
STA = BULLET()
STA.diameter = 6.0
STA.mass = 6.0
STA.velocity = 925.0
STA.calculate()
bullets["STA"] = STA

# DMR (Designated Marksman Round)
DMR = BULLET()
DMR.diameter = 8.0
DMR.mass = 12.0
DMR.velocity = 800.0
DMR.calculate()
bullets["DMR"] = DMR

# AMR (Anti-Material Round)
AMR = BULLET()
AMR.diameter = 14.0
AMR.mass = 45.0
AMR.velocity = 800.0
AMR.calculate()
bullets["AMR"] = AMR



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
        print "%s:" % (bullet)
        print "  Constants:"
        print "    Diameter: %s mm" % (bullets[bullet].diameter)
        print "    Mass: %s grams" % (bullets[bullet].mass)
        print "    Velocity: %s m/s" % (bullets[bullet].velocity)
        print "  Calculated (at muzzle velocity):"
        print "    Drag: %.1f" % (bullets[bullet].drag)
        print "    Power: %.1f kJ" % (bullets[bullet].power/1000.0)
        print "    Recoil/Momentum: %.1f" % (bullets[bullet].momentum)
        print "    Damage: %.1f (kill: %s chest shots, %s limb shots, 1 headshot)\n\n" % (bullets[bullet].damage, calcChestShots(bullets[bullet].damage), calcLimbShots(bullets[bullet].damage))

printBullets()

################################
### ------ ballistics ------ ###
################################
### Copyright 2009 Chase Moskal
INIT = 0

class PROJECTILESYSTEM:

    projectiles = []

    def __init__(self, obj):
        # Needs a gameblender object for raycasting
        self.obj = obj

    def addProjectile(self, owner, startpos, startori, velocity, mass, airdamping, randomness, gravityincrement, terminalvelocity, maxsteps, ticrate=60.0):
        projectile = self.PROJECTILE(self, owner, startpos, startori, velocity, mass, airdamping, randomness, gravityincrement, terminalvelocity, maxsteps, ticrate)
        self.projectiles.append(projectile)

    def removeProjectile(self, projectile):
        self.projectiles.remove(projectile)

    def simulate(self, debug=0):
        for projectile in self.projectiles:
            projectile.simulate(debug)

    class PROJECTILE:
        def __init__(self, projectilesystem, owner, startpos, startori, velocity, mass, airdamping, instability, gravityincrement, terminalvelocity, maxsteps, ticrate):
            self.projectilesystem = projectilesystem
            self.owner = owner
            self.startpos = startpos
            self.startori = startori
            self.velocity = velocity/ticrate
            self.mass = mass
            self.airdamping = airdamping/ticrate
            self.instability = instability/100.0
            self.gravityincrement = gravityincrement/ticrate
            self.terminalvelocity = terminalvelocity
            self.maxsteps = maxsteps
            self.ticrate = ticrate

            self.position = startpos
            self.direction = self.normalize(self.getYFromOri(self.startori))

            self.gravity = 0.0

            self.path = []
            self.terminate = 0
            self.step = 0

            import random
            self.random = random

        def simulate(self, debug=1):
            if self.step > self.maxsteps:
                self.terminate = 1
            
            if not self.terminate:
                
                # Simulate Projectile
                self.doAirDamping()
                self.doInstability()
                self.doGravity()
                self.doProjection()
                self.step += 1

                E = self.getKineticEnergy()
                
                if debug == 1:
                    import Rasterizer
                    line = self.path[len(self.path)-1]
                    Rasterizer.drawLine(line[0], line[1], [1.0, 0.0, 0.0])
                elif debug == 2:
                    import Rasterizer
                    for line in self.path:
                        Rasterizer.drawLine(line[0], line[1], [1.0, 0.0, 0.0])
            else:
                # Terminate Self
                self.projectilesystem.removeProjectile(self)


        ### ================================================================================================
        ### THE SIMULATION
        ### ================================================================================================
        def doProjection(self):
            obj = self.owner

            D = self.direction
            V = self.velocity

            startpos = self.position
            offset = [ D[0]*V, D[1]*V, (D[2]*V)-(self.gravity/self.ticrate) ]
            newpos = self.offset(offset)

            hit, point, normal = obj.rayCast(startpos, newpos)

            if hit:
                self.position = point
                self.terminate = 1
            else:
                self.position = newpos

            self.path.append( [startpos, self.position] )

        def doAirDamping(self):
            if self.velocity > 0.0:
                damping = self.airdamping / self.mass
                damp = self.velocity*damping
                self.velocity -= damp
            else:
                self.velocity = 0.0

        def doInstability(self):
            self.randomizeDirection(self.instability)

        def doGravity(self):
            if self.gravity < self.terminalvelocity:
                self.gravity += self.gravityincrement
            else:
                self.gravity = self.terminalvelocity


        ### ================================================================================================
        ### TOOLS
        ### ================================================================================================
        def getKineticEnergy(self):
            # E = 0.5(mv^2)
            m = self.mass / 1000.0 # Converting mass to Kilograms
            #print "Mass: %s"%(m)
            v = self.velocity*self.ticrate
            #print "Velocity: %s"%(v)
            E = (m/2.0) * (v*v)
            #print "Energy: %s"%(E)
            return E
        
        def randomize(self, x, value=0.1):
            r = self.random.random()
            r *= value
            neg = self.random.choice([1, 0])
            if neg:
                r *= -1.0
            return x+r

        def randomizeDirection(self, value=1.0):
            #value = value/100.0
            x = self.direction[0]
            y = self.direction[1]
            z = self.direction[2]

            X = self.randomize(x, value)
            Y = self.randomize(y, value)
            Z = self.randomize(z, value)

            self.direction = [X, Y, Z]
            self.normalizeDirection()

        def getYFromOri(self, ori):
            # Y = [YX, YY, YZ]
            return [ ori[0][1], ori[1][1], ori[2][1] ]

        def offset(self, offset):
            pos = self.position
            
            X = pos[0]
            Y = pos[1]
            Z = pos[2]

            X += offset[0]
            Y += offset[1]
            Z += offset[2]

            return [X, Y, Z]

        def normalizeDirection(self):
            self.direction = self.normalize(self.direction)

        def normalize(self, vector):
            import math
            L = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
            nVector = [vector[0]/L, vector[1]/L, vector[2]/L]
            return nVector


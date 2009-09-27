### ####################################### ###
### ### ------ BALLISTICS ENGINE ------ ### ###
### ####################################### ###
### # The FPS Project
INIT = 0
manager = None # initiated at bottom

### DEPENDENCIES:
# modules.items.bullets
# modules.time

def dependenciesAreHappy():
    import modules
    return (modules.items.bullets and modules.timetools)

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
        self.bullets = self.modules.items.bullets
        self.timetools= self.modules.timetools

    pool = [] # Pool of bullets to be simulated.
    toTerminalSim = [] # Bullets that need to be removed from pool and handled by Terminal Simulation.
    deadPool = [] # List of bullets that need to be removed from the pool; they are dead.

    def addToSimulation(self, bullet, owner):
        """
        Adds a bullet object to the ballistics simulation.
        """
        # Setting owner object for raycasting
        bullet.owner = owner
        
        # Timer for ballistics simulation. Giving it a 1 frame headstart.
        bullet.timer = self.timetools.TIMER(modules.systems.timetools.perFrame())
        
        # Starting the bullet.path at the bullet's starting point
        bullet.path.append(bullet.position)

        # Adding it to the external simulation pool
        self.pool.append(bullet)

    def run(self):
        self.externalSimulation()
        self.terminalSimulation()




    ### ================================================
    ### External Simulation
    ### ================================================

    def externalSimulation(self):
        """
        Performs external ballistics simulation for each bullet.
        Can divide the bullet pool into multiple passes for simulation
        to divide up the workload (while decreasing authenticity of the
        simulation).
        """
        for bullet in self.pool:
            # The actual simulation for each bullet
            self.eSim(self, bullet)
        self.cleanThePool()

    def cleanThePool(self):
        for deadBullet in self.deadPool:
            self.pool.remove(deadBullet)
        self.deadPool = []



    def eSim(self, bullet):
        """
        The external simulation of a single bullet.
        """
        # Getting the length of time that this simulation step is simulating.
        stepTime = bullet.time.get()
        bullet.time.reset()
        
        self.factorDamping(bullet, stepTime)
        self.factorGravity(bullet, stepTime)
        self.factorRandomness(bullet, stepTime)
        
        self.projectBullet(bullet, stepTime)
            
        if bullet.steps >= bullet.maxsteps:
            # Bullet has run out of simulation time; killing bullet
            self.deadPool.append(bullet)




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
        Projects a ray from current position to the next position,
        if the ray hits an object, then pass bullet to terminal ballistics,
        otherwise set bullet's position to the next position.
        """
        # Using stepTime to get the displacement magnitude for this step.
        M = bullet.velocity * stepTime # Positional displacement Magnitude.
        D = self.normalize(bullet.direction) # 3D Direction Vector

        X = D[0] * M
        Y = D[1] * M
        Z = D[2] * M
        offset = [X, Y, Z] # Local offset from current position to new position

        newPosition = self.offset(bullet.position, offset)
        
        obj = bullet.owner # The object we will use for raycasting
        hit, point, normal = obj.rayCast(position, newPosition) # Raycasting...

        if hit: # If the bullet hit something...
            bullet.position = point # Unnecessary, but it makes sense and might be nifty.

            # Saving the hit data to the bullet
            bullet.hit = hit
            bullet.point = point
            bullet.normal = normal

            # Passing the bullet to the terminal simulation
            self.toTerminalSim.append(bullet) # The bullet is removed from the bullet pool by the terminal simulation

        else:
            # The bullet didn't hit anything, so we can safely
            # move the bullet to the newPosition.
            bullet.position = newPosition

        # Adding the new position to the path (used for drawing the bullet)
        bullet.path.append(newPosition)

        # Incrementing Step Counter
        bullet.step += 1
        









    ### ================================================
    ### Terminal Simulation
    ### ================================================

    def terminalSimulation(self):
        """
        Removes toTerminal bullets from pool and simulates them.
        """
        for bullet in self.toTerminalSim:
            self.pool.remove(bullet)
            # The actual simulation for each bullet
            self.tSim(bullet)
        self.toTerminalSim = []



    def tSim(self, bullet):
        """
        The terminal simulation of a single bullet.
        """
        # Do terminal simulation on bullet here









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


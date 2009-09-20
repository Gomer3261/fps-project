############################
### ------ PLAYER ------ ###
############################
### Copyright 2009 Chase Moskal!
# This module runs the player object.

handler = None

import modules.interface
terminal = modules.interface.terminal

def manage(con):
    global handler, HANDLER

    # Cleanup Dead Handler
    if handler:
        if not handler.LIFE:
            handler = None



# For the spot light casting shadows
def followPlayer(con):
    global handler
    
    playerPos = [0.0, 0.0, 0.0]

    if handler:
        playerPos = handler.pcol.position

    con.owner.position = playerPos





def spawn(con):
    global handler, HANDLER
    if handler:
        raise Exception, "You cannot spawn the local player; the local player is already alive."
    handler = HANDLER(con)
    terminal.output("Player Spawned.")

def kill():
    global handler
    import modules.gamesystems.camera as camera

    if camera.INIT:
        if not handler:
            raise Exception, "You cannot kill the local player; the local player is already dead."
        handler.alive = 0
        camera.reset()
        terminal.output("Player Killed.")
    else:
        raise Exception, "You cannot kill the local player; the local player is already dead"
    
    

class HANDLER:
    LIFE = 1 # This is the object's life, not a representation of the player's life.
    # When this is == 0, it means the player object is gone, and this handler is dead and ready to be cleared.

    import GameLogic
    import Mathutils
    import math

    pcol = None # The Player Collision Box (which is the parent of all of the other game objects that go along with that
    con = None # Controller attached to all the player object's actuators and stuff.

    alive = 1 # Set this to 0 to kill the player.

    stance = 0 # 0=stand, 1=crouch, 2=prone
    HP = 100 # Health.
    stamina = 100 # Used for sprint bar and character fatigue effects

    speedforce = 80.0 # Speed in force of general player movement
    sprintmod = 1.75 # Speed multiplier when sprinting (1.0=no change, 2.0=double)
    jumpforce = 300.0 # Upward force when jump is executed.




    
    def __init__(self, spawnCon):
        import modules
        
        self.spawnCon = spawnCon

        # Spawning the player object (this method also sets self.con)
        self.spawnPcol()
        
        self.YPivot = self.con.actuators["YPivot"].owner
        self.centerhinge = self.con.actuators["centerhinge"].owner
        self.fpcam = self.con.actuators["fpcam"].owner

      
        self.inputs = modules.interface.inputs
        self.terminal = modules.interface.terminal
        self.options = modules.interface.options

        self.mousetools = modules.gamesystems.mousetools
        self.damper = modules.gamesystems.damper



    ### ========================================================================
    ### SPAWN PLAYER OBJECT
    ### ========================================================================
    
    def spawnPcol(self):
        scene = self.GameLogic.getCurrentScene()
        self.pcol = scene.addObject("pcol", self.spawnCon.owner)
        self.pcol.position = [0.0, 0.0, 10.0]
        self.pcol.orientation = [[1,0,0],[0,1,0],[0,0,1]]
        self.con = self.pcol.controllers[0]
        











    ### ========================================================================
    ### HIGH-LEVEL DO FUNCTION
    ### ========================================================================

    def do(self):
        if self.alive:
            self.doCamera() # Deprecated
            self.doPlayerMovement() # Running, Sprinting, Jumping, etc...
            self.doMouseLook() # Looking around with mouse in first person...
            #self.doInventory() # Managing the player's inventory (switching weapons, etc)
            #self.doInteraction() # Using current selected inventory item, interacting with buttons, etc..

        else:
            self.doDeath()
    



    ### ========================================================================
    ### DO CAMERA (Deprecated)s
    ### ========================================================================
    
    def doCamera(self):
        # Deprecated
        pass
        # Just sets the camera
##        if self.LIFE:
##            scene = self.GameLogic.getCurrentScene()
##            if scene.active_camera != self.fpcam:
##                scene.active_camera = self.fpcam








    ### ========================================================================
    ### DO PLAYER MOVEMENT
    ### ========================================================================

    def doPlayerMovement(self):
        X, Y, Z = self.getDesiredMovement()
        X, Y, Z = self.applySprint(X, Y, Z)

        # Slope Damping
        slopeinfluence = 1.0 #change this value to change the ammount of influence slopes have on movement.
        slopefactor = self.calculateSpeedFactor()
        X -= X * (slopefactor * slopeinfluence)
        Y -= Y * (slopefactor * slopeinfluence)
        Z -= Z * (slopefactor * slopeinfluence)

        # Applying the movement
        if not self.terminal.active:
            self.pcol.applyForce([X, Y, Z], 1)

        # Damping Operation
        damp = 25.0
        self.damper.dampXY(self.pcol, damp)

    

    def getDesiredMovement(self):
        # Initial Movement Values (in local coords)
        X = 0.0
        Y = 0.0
        Z = 0.0

        # Input Status
        forward = self.inputs.controller.getStatus("forward")
        backward = self.inputs.controller.getStatus("backward")
        left = self.inputs.controller.getStatus("left")
        right = self.inputs.controller.getStatus("right")

        # Figuring out desired movement
        if forward:
            Y += self.speedforce
        if backward:
            Y -= self.speedforce

        if left:
            X -= self.speedforce
        if right:
            X += self.speedforce

        if X and Y:
            X *= 0.7071
            Y *= 0.7071

        return X, Y, Z



    def getGlobalDesiredMovement(self):
        X, Y, Z = self.getDesiredMovement()
        localmovement = [X, Y, Z]

        if localmovement != [0, 0, 0]:
            orientation = self.pcol.orientation[:]

            localmovement[2] = 0
            globalmovement = [0, 0, 0]


            # Figuring out movement in global terms.
            for i in range(3):
                for j in range(3):
                    globalmovement[j] += orientation[j][i] * localmovement[i]

            globalmovement = self.Mathutils.Vector(globalmovement)
            globalmovement.normalize()
            globalmovement = [globalmovement.x, globalmovement.y, globalmovement.z]

            return globalmovement

        else:
            return localmovement

        

    def applySprint(self, X, Y, Z):
        sprint = self.inputs.controller.isPositive("sprint")
        if sprint:
            X *= self.sprintmod
            Y *= self.sprintmod
            Z *= self.sprintmod
        return X, Y, Z



    def getFloorNormal(self):
        con = self.con

        normals = []
        avgnormal = [0, 0, 0]

        normals.append(con.sensors["foot1"].hitNormal)
        normals.append(con.sensors["foot2"].hitNormal)
        normals.append(con.sensors["foot3"].hitNormal)
        normals.append(con.sensors["foot4"].hitNormal)
        normals.append(con.sensors["foot5"].hitNormal)

        for i in range(5):
            avgnormal[0] += normals[i][0]
            avgnormal[1] += normals[i][1]
            avgnormal[2] += normals[i][2]

        for i in range(3):
            avgnormal[i] /= 5.0
            avgnormal[i] *= -1

        return avgnormal


    def calculateSpeedFactor(self):
        globalmovement = self.getGlobalDesiredMovement()

        if globalmovement == [0, 0, 0]:
            return 0

        floornormal = self.getFloorNormal()

        
        floorvector = self.Mathutils.Vector(floornormal)
        floorvector.normalize()
        floorvector = [floorvector.x, floorvector.y, floorvector.z]

        factor = self.math.sqrt((floorvector[0] - globalmovement[0])**2 + (floorvector[1] - globalmovement[1])**2)

        if factor > 1:
            factor = 1

        factor = 1 - factor

        return factor

        

        
        







    ### ========================================================================
    ### DO MOUSE LOOK
    ### ========================================================================

    def doMouseLook(self):
        ##################################
        ### ------ Mouse Script ------ ###
        ##################################
        # By Chase Moskal

        #====================
        #===   Settings   ===
        #====================

        # X and Y Sensitivity
        mxsens = 5.0
        mysens = 5.0

        # Invert X and/or Y axes?
        invertX = 0
        invertY = 0

        # Settings Override
        import traceback
        try:
            mxsens = self.options.settings["mxsens"]
            mysens = self.options.settings["mysens"]
            invertX = self.options.settings["invertx"]
            invertY = self.options.settings["inverty"]
        except:
            traceback.print_exc()
            print "Player/HANDLER/doMouseLook: Unable to get mouse settings from options.\n"
        
        # Restrict Y axis? (disallow looking upside-down?)
        restrictY = 1



        #=========================
        #===   getting stuff   ===
        #=========================

        import GameLogic as gl
        import Rasterizer
        mousetools = self.mousetools


        

        # For an FPS, set the player collision box to Xpivot,
        # and set up an empty as the Y pivot.
        Ypivot = self.YPivot
        Xpivot = self.pcol




        #=================================
        #===   Real Mouselook Action   ===
        #=================================

        # Little function to check if something
        # is positive (>=0)
        def isPositive(x):
            if x >= 0.0:
                return 1
            return 0


        # Shortcut to the mouse object
        mouse = mousetools.mouse
        # Hiding the mouse cursor
        mouse.hide()



        if True:
            
            # Getting mouse movement...
            Xmovement, Ymovement = mouse.getMovement()
            
            # Converting sensitivity to lower terms
            Xc = mxsens * 0.001
            Yc = mysens * 0.001
            
            # Getting the rotation values.
            X = -float(Xmovement) * Xc
            Y = float(Ymovement) * Yc
            
            # Inversions
            if invertX:
                X *= -1
            if invertY:
                Y *= -1
            
            # Getting orientation matrix
            # information that will determine the
            # mouselook Y restrictions.
            
            isMovingUp = isPositive(Y) # checks if the mouse movement is currently up (1) or down (0)
            
            ori = Ypivot.orientation
            
            # Getting uprightness.
            ZZ = ori[2][2] # Z axis' Z component
            isUpright = isPositive(ZZ) # 1 means it's upright, 0 means it's upside-down.
            
            # Getting the facing upness
            YZ = ori[2][1] # Y axis' Z component
            isFacingUp = isPositive(YZ)
            # Imagine the user on a perfectly smooth floor that spans infinitely into the distance.
            # isFacingUp tells you if the player is looking at the floor (0), or at the sky (1).
            
            
            
            
            #===============================
            #===   Applying X Rotation   ===
            #===============================
            
            # If we're not restricting the Y axis, and we're upside down,
            # then we need to invert the X axis mouse movement.
            if (not restrictY) and (not isUpright):
                Xpivot.applyRotation([0, 0, -X], 0)
            else:
                Xpivot.applyRotation([0, 0, X], 0)
            
            
            #===============================
            #===   Applying Y Rotation   ===
            #===============================
            if restrictY:
                # Y Axis is restricted
                
                # Only allows movement while upright
                if isUpright:
                    Ypivot.applyRotation([Y, 0, 0], 1)
                
                # While not upright and you're facing down, allow you to look up again
                elif isMovingUp and not isFacingUp:
                    Ypivot.applyRotation([Y, 0, 0], 1)
                
                # While not upright and you're facing up, allow you to look down again
                elif not isMovingUp and isFacingUp:
                    Ypivot.applyRotation([Y, 0, 0], 1)
            
            else:
                # Y Axis is NOT restricted
                Ypivot.applyRotation([Y, 0, 0], 1)









    ### ========================================================================
    ### DO DEATH
    ### ========================================================================
    
    def doDeath(self):
        if self.LIFE:
            scene = self.GameLogic.getCurrentScene()
            if scene.active_camera != self.fpcam:
                self.pcol.endObject()
                self.LIFE = 0

        

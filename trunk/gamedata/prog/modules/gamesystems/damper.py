############################
### ------ DAMPER ------ ###
############################
### Copyright 2009 Chase Moskal!
# This simple system applies force in the opposite direction
# of an object's velocity to create a simple damping effect.
INIT = 1


def dampify(v, res=10.0):
    f = (v * -1) * res
    return f

# Basic omni-directional damping.
def damp(obj, resistance=10.0):
    vel = obj.getVelocity()
    vx = vel[0]
    vy = vel[1]
    vz = vel[2]
    
    fx = dampify(vx, resistance)
    fy = dampify(vy, resistance)
    fz = dampify(vz, resistance)
    
    obj.applyForce([fx, fy, fz], 0)

# Applies the damping to only X and Y axes.
# Good for character physics.
def dampXY(obj, resistance=10.0):
    vel = obj.getVelocity()
    
    vx = vel[0]
    vy = vel[1]
    # vz = vel[2]
    
    fx = dampify(vx, resistance)
    fy = dampify(vy, resistance)
    # fz = dampify(vz, resistance)
    
    obj.applyForce([fx, fy, 0.0], 0)

# This method is deprecated and may soon be removed.
def getLocalVelocity(obj):
    vel = obj.getLinearVelocity()
    ori = obj.getOrientation()

    vx = [vel[0], 0.0, 0.0]
    vy = [0.0, vel[1], 0.0]
    vz = [0.0, 0.0, vel[2]]

    vel = [vx, vy, vz]

    LocVel = []
    for r in [0, 1, 2]:
        row = []
        for c in [0, 1, 2]:
            row.append( (vel[r][0]*ori[0][c]) + (vel[r][1]*ori[1][c]) + (vel[r][2]*ori[2][c]) )
        LocVel.append(row)
        
    LVelX = LocVel[0][0] + LocVel[1][0] + LocVel[2][0]
    LVelY = LocVel[0][1] + LocVel[1][1] + LocVel[2][1]
    LVelZ = LocVel[0][2] + LocVel[1][2] + LocVel[2][2]

    return [LVelX, LVelY, LVelZ]

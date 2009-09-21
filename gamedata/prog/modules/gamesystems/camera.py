# Just contains stuff for doing camera operations.
INIT = 0
ecam = None




import GameLogic
scene = GameLogic.getCurrentScene()

def init(con):
    global INIT
    global ecam
    ecam = con.actuators["ecam"].owner
    INIT = 1
    print "Camera Initiated"

def initLoop(con):
    global INIT

    if not INIT:
        init(con)






def reset():
    global scene
    global ecam

    scene.active_camera = ecam






def run(con):
    global scene
    global ecam

    initLoop(con)

    import modules
    player = modules.gamesystems.player

    cam = ecam

    # Player Camera
    if player.handler:
        if player.handler.alive:
            cam = player.handler.fpcam

    scene.active_camera = cam
        

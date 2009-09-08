### ================================================ ================================================
### ------------------------------------------------ ------------------------------------------------

import modules

masterserver = modules.masterserver.masterserver
gameplayclient = modules.gameplayclient

### ================================================ ================================================
### CONNECT TO MASTER SERVER
### ================================================ ================================================

### INITIATION ###
if (not server.connected):
    # connect (host, masterserverport, gameplayTCPport, gameplayUDPport)name, flag, data, addr
    server.connect("chase.kicks-ass.net", 2346, 2342, 2343)

### MAIN LOOP ###
while 1:
    if server.connected:

        # Networking
        server.doNetworking()

        # Interaction
        server.interact()

        # Gameplay
        server.play()

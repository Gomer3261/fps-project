import modules

gameplayserver = modules.gameplayserver
server = gameplayserver.server

print """
  ///////////////////////////
 /// The Gameplay Server ///
///////////////////////////
"""

# Connect (MasterServerHost, MasterServerPort, TCP_port, UDP_port)
server.connect("chase.kicks-ass.net", 2340, 2342, 2343)

### MAIN LOOP ###
if server.connected:
    print "\n~~~ Server is now running happily :D ~~~\n"
    while server.LIFE:
            # Networking
            server.doNetworking()

            # Interaction
            server.interact()

            # Gameplay
            server.play()

    print "\nJob done."
else:
    print "Server could not connect; cannot continue. If you need help running this server, contact Chase at chasemoskal@gmail.com"

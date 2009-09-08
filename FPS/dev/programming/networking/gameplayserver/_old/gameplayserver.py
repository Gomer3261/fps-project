###########################################
###### ------ GAMEPLAY SERVER ------ ######
###########################################
### Copyright 2009 Chase Moskal
# The Gameplay Server is structurally derived from
# the Master server.

class GAMEPLAYSERVER:
    import gpsclasses
    SOCKETS = gpsclasses.SOCKETS
    HANDLER = gpsclasses.HANDLER
    CLIENT = gpsclasses.CLIENT
    MASTERSERVER = gpsclasses.MASTERSERVER

    LIFE = 1

    clients = []
    masterserver = None

    info = {}
    info["servername"] = "Chaser's Gameplay Server"
    info["serverinfo"] = "Currently in testing"
    info["message"] = "I enjoy bacon and sushi."

    def __init__(self, cport=2342, sport=2341):
        self.sockets = self.SOCKETS(cport, sport)
        self.masterserver = self.MASTERSERVER(self.sockets.masterserversocket, 240.0)
        print "\n======      GAMEPLAY SERVER UP AND RUNNING      ======\n\n"

    def run(self):
        while self.LIFE:
            self.doNetworking()
            self.doTasks()



    ################################################
    ###### ------ TASK RELATED METHODS ------ ######
    ################################################

    def doTasks(self):
        self.interactWithClients()
        self.interactWithMasterServer()




    def interactWithClients(self):
        import comms

        ### CLIENT INTERACTION ###
        for client in self.clients:
            client.sendloop() # Asynchronous send loop to handle send-buffer overflow.
            packages = client.recv(2048)
            for package in packages:
                flag, data = comms.unpack(package)
                print "        '%s' Package received from client %s." % (flag, client.getName())

                flag = flag.lower()
                
                if flag == "echo":
                    client.send(flag, data)
                    print "        Package echoed back."

                elif flag == "query":
                    client.send("info", self.info)
                    print "        Sent info."


    def interactWithMasterServer(self):
        import comms
        masterserver = self.masterserver
        masterserver.sendloop()
        packages = masterserver.recv(2048)
        for package in packages:
            flag, data = comms.unpack(package)
            print "        '%s' package from master server." % (flag)
            flag = flag.lower()

            if flag == "echo":
                masterserver.send(flag, data)
                
            elif flag == "query":
                masterserver.send("info", self.info)

            elif flag == "ping":
                masterserver.send("PONG", 1)






    
    ######################################################
    ###### ------ NETWORKING RELATED METHODS ------ ######
    ######################################################
    
    def doNetworking(self):
        self.acceptClient()
        self.ejectStaleClients()
        self.cleanUp()

    def acceptClient(self):
        newClientConnection = self.sockets.acceptClient()
        if newClientConnection:
            client = self.CLIENT( newClientConnection )
            self.clients.append(client)
            print ">>> New Client Connection: %s; %s clients remain." % (client.getName(), len(self.clients))

    def ejectStaleClients(self):
        for client in self.clients:
            clientWasEjected = client.ejectIfStale()
            if clientWasEjected:
                print "        Client %s went stale." % (client.getName())

    def cleanUp(self):
        deadClients = []
        for client in self.clients:
            if not client.LIFE:
                deadClients.append(client)
        for deadClient in deadClients:
            self.clients.remove(deadClient)
            print "    Client %s was terminated and has been cleaned up. %s clients remain." % (deadClient.getName(), len(self.clients))
            del deadClient

    def terminate(self):
        print ">>> Terminating MasterServer..."
        for client in self.clients:
            client.terminate()
        self.cleanUp()
        self.sockets.terminate()
        self.LIFE = 0

        print "\n====== ------ GAMEPLAY SERVER TERMINATED ------ ======\n"








GameplayServer = GAMEPLAYSERVER(2342, 2346)
GameplayServer.run()

#########################################
#########################################
###### ------ MASTER SERVER ------ ######
#########################################
#########################################
### Copyright 2009 Chase Moskal

class MASTERSERVER:
    LIFE = 1
    
    import msclasses
    MASTERSERVERSOCKETS = msclasses.MASTERSERVERSOCKETS
    HANDLER = msclasses.HANDLER

    import theater
    clientTheater = theater.THEATER()

    info = {}
    info["servername"] = "Official Master Server"
    info["serverinfo"] = "Currently in testing"
    info["message"] = "Greetings from the Master Server!"
    info["clients"] = ""
    info["servers"] = ""

    lastClientCheck = 0.0

    def __init__(self, cport=2340, sport=2341):
        self.sockets = self.MASTERSERVERSOCKETS(cport, sport)
        print "\n====== ------ MASTERSERVER UP AND RUNNING ------ ======\nClientPort: %s\nServerPort: %s\n\n" % (cport, sport)

    def run(self):
        while self.LIFE:
            self.doNetworking()
            self.doTasks()


    ################################################
    ###### ------ TASK RELATED METHODS ------ ######
    ################################################

    def doTasks(self):
        self.interactWithClients()
        self.checkClients()

    def checkClients(self, t=10.0):
        import time

        dif = time.time() - self.lastClientCheck
        if dif > t:
            for ticket in self.clientTheater.seats:
                seat = self.clientTheater.seats[ticket]
                client = seat.handler
                if client:
                    client.send("CHECK", 1)
            self.lastClientCheck = time.time()
    
    def interactWithClients(self):
        theater = self.clientTheater
        
        import comms
        import database
        accounts = database.accounts

        ### CLIENT INTERACTION ###
        for ticket in theater.seats:
            seat = theater.seats[ticket]
            client = seat.handler
            if client:
                client.sendloop() # Asynchronous send loop to handle send-buffer overflow.
                packages = client.recv(2048)
                for package in packages:
                    flag, data = comms.unpack(package)
                    #print "        '%s' Package received from client (%s)." % (flag, client.ip)
                    flag = flag.lower()
                    
                    if flag == "echo":
                        client.send(flag, data)
                        print "        Package echoed back."

                    elif flag == "claim":
                        client.send("TICKET", ticket)
                        print "        Client (%s) is requesting their ticket, which is: %s." % (client.ip, ticket)

                    elif flag == "reclaim":
                        newTicket = data
                        print "    Client (%s) is reclaiming %s." % (client.ip, newTicket)
                        success = theater.reclaim(ticket, newTicket)
                        if success:
                            client.send("GOOD", "Your session has been restored.")
                        else:
                            client.send("BAD", "The session with ticket %s could not be restored."%(newTicket))

                    elif flag == "check":
                        pass

                    elif flag == "query":
                        self.info["clients"] = len(theater.seats)
                        self.info["servers"] = 0
                        client.send("info", self.info)
                        print "        Client (%s) Query'd." % (client.ip)
                        
                    elif flag == "disconnect":
                        # Terminates this entire seat (and the client's connection with it)
                        seat.terminate()

                    elif flag == "break":
                        # Terminates this entire seat (and the client's connection with it)
                        client.terminate()

                    elif flag == "terminate":
                        print "        This means the master server should completely terminate."
                        self.terminate()

                    elif flag == "newaccount":
                        print "        Creating account..."
                        name = data["name"]
                        password = data["password"]
                        email = data["email"]
                        if not accounts.inIndex(name):
                            account = accounts.createAccount(name, password, email)
                            result = accounts.saveAccount(account)
                            if result:
                                client.send("GOOD", "Account created successfully!")
                                print "        Account created."
                            else:
                                client.send("BAD", "An error occurred while creating your account! :(")
                                print "        Yikes! Some kind of error occurred while trying to create %s's account!" % (name)
                        else:
                            msg = """An account for username "%s" already exists""" % (name)
                            client.send("BAD", msg)
                            print "        Account already existed."
                    
                    elif flag == "login":
                        if (not seat.info["loggedIn"]):
                            # CU for Current User
                            CU_name = data["name"]
                            CU_password = data["password"]

                            print "        Client is trying to go online as '%s'..." % (CU_name)

                            if not accounts.inIndex(CU_name):
                                print "        Account does not exist."
                                client.send("BAD", "Account does not exist.")
                                return 0
                            
                            # AC for Account
                            account = accounts.getAccount(CU_name)
                            AC_name = account["info"]["name"]
                            AC_password = account["info"]["password"]

                            if CU_password != AC_password:
                                client.send("BAD", "Incorrect password.")
                                print "        Incorrect password."
                                return 0

                            client.info["loggedIn"] = AC_name

                            client.send("GOOD", "You are now online as %s"%(AC_name))
                            print "        %s is now online as %s" % (ticket, AC_name)
                        else:
                            # Is already logged in
                            client.send("BAD", "You cannot login because you are already logged in as '%s'." % (client.info["loggedIn"]))

                    elif flag == "logout":
                        # Only works when client is logged in
                        if client.info["loggedIn"]:
                            cname = client.info["loggedIn"]
                            # Removing the client's loggedIn status.
                            client.info["loggedIn"] = ""
                            print "        %s is now offline." % (cname)
                            client.send("GOOD", "You have been successfully logged out.")
                        else:
                            client.send("BAD", "You cannot logout if you are not logged in; you are not logged in.")
    #

    ######################################################
    ###### ------ NETWORKING RELATED METHODS ------ ######
    ######################################################
    
    def doNetworking(self):
        self.acceptConnections()
        self.terminateStaleStuff()
        self.cleanUp()

    def acceptConnections(self, clientTimeout=21.0, serverTimeout=61.0):
        newClientConnection, newServerConnection = self.sockets.acceptConnections()
        if newClientConnection:
            client = self.HANDLER( newClientConnection, clientTimeout )
            ticket = self.clientTheater.seatHandler(client)
            seat = self.clientTheater.seats[ticket]
            seat.info["loggedIn"] = ""
            print ">>> New Client Connection: (%s); There are now %s clients." % (client.ip, len(self.clientTheater.seats))

    def terminateStaleStuff(self):
        for ticket in self.clientTheater.seats:
            seat = self.clientTheater.getSeat(ticket)

            client = seat.handler
            if client:
                clientWasTerminated = client.terminateIfStale()
                if clientWasTerminated:
                    seat.setLastTime()
                    seat.handler = None
                    print "        (%s) was terminated" % (client.ip)
            else:
                seatWasTerminated = seat.terminateIfStale()
                if seatWasTerminated:
                    print "    %s was terminated." % (ticket)

    def cleanUp(self):
        self.clientTheater.cleanUp()

    def terminate(self):
        print ">>> Terminating MasterServer..."
        self.clientTheater.terminateAll()
        self.cleanUp()
        self.sockets.terminate()
        self.LIFE = 0

        print "\n====== ------ MASTERSERVER TERMINATED ------ ======\n"

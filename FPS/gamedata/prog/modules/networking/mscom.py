### For asynchronous communication with the Master Server
INIT = 0

class HANDLER:
    import asynsock
    sock = asynsock.ASYNSOCK()

    ### IMPORTANT ###
    # Keep in mind that 'sock' is
    # actually an ASYNSOCK object,
    # not a socket object.

    operation = None
    operationQueue = []

    connected = 0
    loggedIn = ""
    ticket = 0

    def __init__(self, modules):
        self.terminal = modules.systems.terminal
        self.notifications = modules.systems.notifications

    def output(self, text):
        self.terminal.output(text)
        self.notifications.notify(text)

    def setStatus(self, key, value):
        import GameLogic
        GameLogic.globalDict["msinfo"][key] = value
    
    def cleanUp(self):
        for operation in self.operations:
            if not operation.LIFE:
                self.operations.remove(operation)

    def cancelOperation(self):
        self.operation = None
        self.operationQueue = []

    def run(self):
        # mmkay, so this is the run function.
        # it goes through the operation queue, and
        # runs each operation until it's finished,
        # which is when operation.LIFE == 0.

        # when there are no operations, it will
        # perform CHECK echoes with the server to
        # stay connected.
        
        if self.operation:
            if self.operation.LIFE:
                self.operation.run()
            else:
                self.operation = None
        else:
            if self.operationQueue:
                self.operation = self.operationQueue[0]
                self.operationQueue.pop(0)
                self.operation.run()
            else:
                self.operation = None
                if self.connected:
                    try:
                        pairs = self.recv(4096, 21.0)
                    except:
                        # Gone stale.
                        self.handler.output("Connection to master server has been lost.")
                        self.clear()

    def addOperation(self, operation):
        self.operationQueue.append(operation)

    def recv(self, buf=4096, timeout=61.0):
        # The reason we have to use this recv() call
        # instead of sock.recv(), is because
        # this one filters out and responds to
        # CHECK calls so that they do not get
        # mixed in with an operation.
        
        packages = self.sock.recv(buf, timeout)
        import comms
        pairs = comms.unpackList(packages)

        goodPairs = []
        
        for pair in pairs:
            flag = pair[0]
            data = pair[1]
            if flag.lower() == "check":
                self.sock.send("CHECK", 1)
                self.sock.sendloop()
            else:
                goodPairs.append( (flag, data) )
        return goodPairs

    def clear(self):
        self.sock.clear()
        self.operation = None
        self.operationQueue = []
        
        self.connected = 0
        self.loggedIn = ""
        self.ticket = 0

mscomHandler = None




### ==================================== ====================================
### TEMPLATE Operation
### ==================================== ====================================

class OPERATION:
    LIFE = 1
    def __init__(self, handler):
        self.handler = handler
        self.sock = handler.sock
        
        self.terminal = handler.terminal
        self.Notifier = handler.notifications.Notifier

    step = 0

    def run(self):
        import traceback
        try:
            if not self.handler.connected:
                self.handler.output("You cannot query the master server; you are not connected.")
                self.LIFE = 0
                return 0, "Not connected"

            if self.step == 0:
                self.sock.send("QUERY", 1)
                self.step = 1

            if self.step == 1:
                completed = self.sock.sendloop(5.0)
                if completed:
                    self.step = 2

            if self.step == 2:
                pairs = self.handler.recv(4096, 5.0)
                for pair in pairs:
                    flag = pair[0]
                    data = pair[1]
                    
                    if flag.lower() == "info":
                        for key in data:
                            self.handler.output("-%s: %s"%(key, data[key]))
                        self.LIFE = 0
                        return 1, "Query completed"
                    else:
                        self.handler.output("Query operation failed: %s" % (data))
                        self.LIFE = 0
                        return 0, "Query operation failed: %s" % (data)
        except:
            traceback.print_exc()
            self.LIFE = 0










### ==================================== ====================================
### Connect Operation
### ==================================== ====================================

class CONNECT:
    LIFE = 1
    
    def __init__(self, handler, host="chase.kicks-ass.net", port=2340):
        self.handler = handler
        self.sock = handler.sock
        
        self.terminal = handler.terminal
        self.Notifier = handler.notifications.Notifier
        
        self.host = host
        self.port = port

    def run(self):
        import traceback
        if not self.handler.connected:
            try:
                if not self.sock.connecting:
                    self.terminal.output("Attempting connection...")
                connected = self.sock.connect(self.host, self.port, 10.0)
                if connected:
                    self.handler.output("You are now connected to the master server!")
                    self.LIFE = 0
                    
                    self.handler.connected = 1
                    return 1, "You are now connected to the master server"
                else:
                    return 1, "Connection operation still in progress"
            except:
                traceback.print_exc()
                # There was an error connecting to the master server.
                self.handler.output("Unable to connect to master server.")
                self.LIFE = 0
                
                self.handler.connected = 0
                return 0, "Unable to connect to master server"
        else: # Handler is already connected
            self.handler.output("You are already connected.")
            self.LIFE = 0
            return 1, "Already connected"



### ==================================== ====================================
### Login Operation
### ==================================== ====================================

class LOGIN:
    LIFE = 1
    def __init__(self, handler, name, password):
        self.handler = handler
        self.sock = handler.sock
        
        self.terminal = handler.terminal
        
        self.name = name
        self.password = password

    step = 0

    def run(self):
        import traceback
        try:
            if not self.handler.connected:
                self.handler.output("You cannot login because you are not connected.")
                self.LIFE = 0
                return 0, "Not connected"

            if self.step == 0:
                self.sock.send("LOGIN", {"name":self.name, "password":self.password})
                self.step = 1

            if self.step == 1:
                completed = self.sock.sendloop(5.0)
                if completed:
                    self.step = 2

            if self.step == 2:
                #print "RECV: %s" % (self.handler.lastTime)
                pairs = self.handler.recv(4096, 5.0)
                for pair in pairs:
                    flag = pair[0]
                    data = pair[1]
                    
                    if flag.lower() == "good":
                        self.handler.output(data)

                        self.handler.setStatus("loggedIn", self.name)
                        self.handler.loggedIn = self.name
                        self.LIFE = 0
                        return 1, "You're logged in"
                    else:
                        self.handler.output("Login operation failed: %s" % (data))
                        self.LIFE = 0
                        return 0, "Login operation failed: %s" % (data)
        except:
            traceback.print_exc()
            self.terminal.output("Could not login; it seems like the connection has failed or something man.")
            self.LIFE = 0





### ==================================== ====================================
### Break Operation
### ==================================== ====================================

class BREAK:
    LIFE = 1
    def __init__(self, handler):
        self.handler = handler
        self.sock = handler.sock

        self.terminal = handler.terminal

    step = 0

    def run(self):
        import traceback
        try:
            if not self.sock.connected:
                self.handler.output("You cannot break because you are not yet connected")
                self.LIFE = 0
                return 0, "Not connected"

            if self.step == 0:
                self.sock.send("BREAK", 1)
                self.step = 1

            if self.step == 1:
                try:
                    completed = self.sock.sendloop(5.0)
                    if completed:
                        self.step = 2
                except:
                    self.step = 2

            if self.step == 2:
                #self.handler.clear()
                self.handler.connected = 0
                self.handler.output("You have temporarily broken from server connection. You can reclaim your session.")
                self.LIFE = 0
        except:
            traceback.print_exc()
            self.LIFE = 0



### ==================================== ====================================
### DISCONNECT Operation
### ==================================== ====================================

class DISCONNECT:
    LIFE = 1
    def __init__(self, handler):
        self.handler = handler
        self.sock = handler.sock

        self.terminal = handler.terminal

    step = 0

    def run(self):
        import traceback
        try:
            if not self.sock.connected:
                self.handler.output("You cannot disconnect because you are not yet connected")
                self.LIFE = 0
                return 0, "Not connected"

            if self.step == 0:
                self.sock.send("DISCONNECT", 1)
                self.step = 1

            if self.step == 1:
                try:
                    completed = self.sock.sendloop(5.0)
                    if completed:
                        self.step = 2
                except:
                    self.step = 2

            if self.step == 2:
                self.handler.clear()
                self.LIFE = 0

                self.handler.connected = 0

                self.handler.setStatus("loggedIn", "")
                self.handler.setStatus("ticket", 0)
                self.handler.loggedIn = ""
                self.handler.ticket = 0
                self.handler.output("Disconnected.")
        except:
            traceback.print_exc()
            self.LIFE = 0




### ==================================== ====================================
### Register New Account Operation
### ==================================== ====================================

class REGISTER:
    LIFE = 1
    def __init__(self, handler, name, password, email):
        self.handler = handler
        self.sock = handler.sock
        
        self.terminal = handler.terminal
        
        self.name = name
        self.password = password
        self.email = email

    step = 0

    def run(self):
        import traceback
        try:
            if not self.handler.connected:
                self.handler.output("You cannot register an account, because you are not connected.")
                self.LIFE = 0
                return 0, "Not connected"

            if self.step == 0:
                self.sock.send("NEWACCOUNT", {"email":self.email, "name":self.name, "password":self.password})
                self.step = 1

            if self.step == 1:
                completed = self.sock.sendloop(10.0)
                if completed:
                    self.step = 2

            if self.step == 2:
                pairs = self.handler.recv(4096, 10.0)
                for pair in pairs:
                    flag = pair[0]
                    data = pair[1]
                    
                    if flag.lower() == "good":
                        self.handler.output(data)
                        self.LIFE = 0
                        return 1, data
                    else:
                        self.handler.output("Registration operation failed: %s" % (data))
                        self.LIFE = 0
                        return 0, "Registration operation failed: %s" % (data)
        except:
            traceback.print_exc()
            self.LIFE = 0



### ==================================== ====================================
### Query Operation
### ==================================== ====================================

class QUERY:
    LIFE = 1
    def __init__(self, handler):
        self.handler = handler
        self.sock = handler.sock
        
        self.terminal = handler.terminal

    step = 0

    def run(self):
        import traceback
        try:
            if not self.handler.connected:
                self.handler.output("You cannot query the master server; you are not connected.")
                self.LIFE = 0
                return 0, "Not connected"

            if self.step == 0:
                self.sock.send("QUERY", 1)
                self.step = 1

            if self.step == 1:
                completed = self.sock.sendloop(5.0)
                if completed:
                    self.step = 2

            if self.step == 2:
                pairs = self.handler.recv(4096, 5.0)
                for pair in pairs:
                    flag = pair[0]
                    data = pair[1]
                    
                    if flag.lower() == "info":
                        self.handler.output("Query Results:")
                        for key in data:
                            self.handler.output("-%s: %s"%(key, data[key]))
                        self.LIFE = 0
                        return 1, "Query completed"
                    else:
                        self.handler.output("Query operation failed: %s" % (data))
                        self.LIFE = 0
                        return 0, "Query operation failed: %s" % (data)
        except:
            traceback.print_exc()
            self.LIFE = 0







### ==================================== ====================================
### Logout Operation
### ==================================== ====================================

class LOGOUT:
    LIFE = 1
    def __init__(self, handler):
        self.handler = handler
        self.sock = handler.sock
        
        self.terminal = handler.terminal
        self.Notifier = handler.notifications.Notifier

    step = 0

    def run(self):
        import traceback
        try:
            if not self.handler.connected:
                self.handler.output("You cannot logout; you are not even connected.")
                self.LIFE = 0
                return 0, "Not connected"

            if self.step == 0:
                self.sock.send("LOGOUT", 1)
                self.step = 1

            if self.step == 1:
                completed = self.sock.sendloop(5.0)
                if completed:
                    self.step = 2

            if self.step == 2:
                pairs = self.handler.recv(4096, 5.0)
                for pair in pairs:
                    flag = pair[0]
                    data = pair[1]
                    
                    if flag.lower() == "good":
                        self.handler.output("You have successfully logged out.")

                        self.handler.setStatus("loggedIn", "")
                        self.handler.loggedIn = ""
                        self.LIFE = 0
                        return 1, "Logged out"
                    else:
                        self.terminal.output("Logout failed: %s" % (data))
                        self.LIFE = 0
                        return 0, "Logout failed: %s" % (data)
        except:
            traceback.print_exc()
            self.LIFE = 0





### ==================================== ====================================
### BRB Operation: DEPRECATED
### ==================================== ====================================

# This one inherits from the template!
class BRB(OPERATION):
    def run(self):
        import traceback
        try:
            if not self.handler.connected:
                self.handler.output("You cannot BRB; you are not even connected.")
                self.LIFE = 0
                return 0, "Not connected"

            if self.step == 0:
                self.sock.send("CLAIM", 1)
                self.step = 1

            if self.step == 1:
                completed = self.sock.sendloop(5.0)
                if completed:
                    self.step = 2

            if self.step == 2:
                pairs = self.handler.recv(4096, 5.0)
                for pair in pairs:
                    flag = pair[0]
                    data = pair[1]
                    
                    if flag.lower() == "ticket":
                        ticket = data
                        self.handler.ticket = ticket
                        self.handler.output("Your ticket is %s"%(ticket))
                        self.step = 3
                    else:
                        self.handler.output("BRB failed: %s" % (data))
                        self.LIFE = 0
                        return 0, "BRB failed: %s" % (data)

            if self.step == 3:
                self.sock.send("DISCONNECT", 1)
                    
            if self.step == 4:
                try:
                    completed = self.sock.sendloop(5.0)
                    if completed:
                        self.step = 5
                except:
                    self.step = 5

            if self.step == 5:
                self.handler.clear()
                self.LIFE = 0
                self.handler.output("BRB Succeeded: You are now disconnected.\nYou may reconnect and reclaim your session with:\nreclaim <ticket>")
                self.Notifier.notify("You are now disconnected.")
                
        except:
            self.handler.output("BRB Failed: Something went wrong; perhaps the connection was lost?")
            traceback.print_exc()
            self.LIFE = 0







### ==================================== ====================================
### CLAIM Operation
### ==================================== ====================================

# This one inherits from the template!
class CLAIM(OPERATION):
    def run(self):
        import traceback
        try:
            if not self.handler.connected:
                self.handler.output("You cannot claim; you are not even connected.")
                self.LIFE = 0
                return 0, "Not connected"

            if self.step == 0:
                self.sock.send("CLAIM", 1)
                self.step = 1

            if self.step == 1:
                completed = self.sock.sendloop(5.0)
                if completed:
                    self.step = 2

            if self.step == 2:
                pairs = self.handler.recv(4096, 5.0)
                for pair in pairs:
                    flag = pair[0]
                    data = pair[1]
                    
                    if flag.lower() == "ticket":
                        ticket = data

                        self.handler.setStatus("ticket", ticket)
                        self.handler.ticket = ticket
                        self.handler.output("Claim succeeeded: Your ticket is %s"%(ticket))
                        self.LIFE = 0
                    else:
                        self.handler.output("Claim failed: %s" % (data))
                        self.LIFE = 0
                        return 0, "Claim failed: %s" % (data)
                
        except:
            self.handler.output("Claim Failed: Something went wrong; perhaps the connection was lost?")
            traceback.print_exc()
            self.LIFE = 0






### ==================================== ====================================
### RECLAIM Operation
### ==================================== ====================================

class RECLAIM(OPERATION):
    def __init__(self, handler, ticket):
        self.handler = handler
        self.sock = handler.sock
        
        self.terminal = handler.terminal
        
        self.ticket = ticket

    def run(self):
        import traceback
        try:
            if not self.handler.connected:
                self.handler.output("You cannot do this; you are not connected.")
                self.LIFE = 0
                return 0, "Not connected"

            if self.step == 0:
                self.sock.send("RECLAIM", self.ticket)
                self.step = 1

            if self.step == 1:
                completed = self.sock.sendloop(5.0)
                if completed:
                    self.step = 2

            if self.step == 2:
                pairs = self.handler.recv(4096, 5.0)
                for pair in pairs:
                    flag = pair[0]
                    data = pair[1]
                    
                    if flag.lower() == "good":
                            self.handler.output("Reclaim successful: %s"%(data))
                            self.LIFE = 0
                    else:
                        self.handler.output("Reclaim operation failed: %s" % (data))
                        self.LIFE = 0
                        return 0, "Reclaim operation failed: %s" % (data)
        except:
            self.handler.output("Reclaim operation failed. Maybe the connection has been lost?")
            traceback.print_exc()
            self.LIFE = 0

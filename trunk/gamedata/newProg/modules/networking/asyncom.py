# For Asynchronous Communication Operations running in the Game Engine

class HANDLER:
    import socket
    import comms
    import time

    asynsock = None




    ################
    ### ASYNSOCK ###
    ################
    ### Class
    class ASYNSOCK:
        import socket
        import comms
        import time

        instream = comms.STREAM()
        outpipe = ""

        lastTime = time.time()

        sock = None
        connected = 0
        connectionOperation = 0

        def setLastTime(self):
            time = self.time
            self.lastTime = time.time()

        def goneStale(self, timeout=5.0):
            time = self.time
            dif = time.time() - self.lastTime
            if dif > timeout:
                return 1
            else:
                return 0

        def createSocket(self):
            import socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setblocking(0)
            self.sock.settimeout(0.0)

        def recv(self, buf=2048):
            if not self.connected:
                raise Exception, "Cannot recv(); Not connected."

            if not self.goneStale():
                try:
                    data = self.sock.recv(buf)
                    if data:
                        self.setLastTime()
                        
                        self.instream.push(data)

                        packages = self.instream.extract()
                        return packages # A list of pairs that look like (flag, data).
                except:
                    pass
            else:
                # Gone stale!
                raise Exception, "Gone stale on recv()"

            return [] # No data.

        def send(self, datapair=None):
            if not self.connected:
                raise Exception, "Cannot send(); Not connected."

            if datapair:
                data = self.comms.pack(datapair[0], datapair[1])
                self.outpipe += data

            if not self.outpipe:
                return 1 # Data sent successfully.

            if not self.goneStale():
                try:
                    sent = self.sock.send(self.outpipe)
                    self.outpipe = self.outpipe[sent:]
                    if sent:
                        self.setLastTime()
                except:
                    pass
            else:
                # Gone stale
                raise Exception, "Gone stale on send()"

            return 0 # Send operation still in progress

        def connect(self, ip="chase.kicks-ass.net", port=2340):
            if not self.sock:
                self.createSocket()

            if self.connectionOperation:
                if self.goneStale():
                    self.sock = None
                    self.connected = 0
                    self.connectionOperation = 0
                    raise Exception, "Connection operation went stale"
                else:
                    try:
                        peer = self.sock.getpeername()
                        if peer:
                            # We're connected!
                            self.connected = 1
                            self.connectionOperation = 0
                            return 1 # Connected!
                    except:
                        pass
            # Not connectionOperation, so we must start connectionOperation
            else:
                try:
                    self.sock.connect( (ip, port) )
                except:
                    pass
                self.connectionOperation = 1
                self.setLastTime() # Setting lastTime for timeout reasons

            return 0 # This means the connection operation is still in progress (this method must be run again)

        def clear(self):
            # Terminate socket
            if self.connected:
                self.sock.close()

            self.sock = None
            self.connected = 0
            self.connectionOperation = 0
            self.setLastTime()
            self.instream = self.comms.STREAM()
            self.outstream = ""




    ### HANDLER FUNCTIONS ###

    def __init__(self):
        self.asynsock = self.ASYNSOCK() # Instantiating asynsock

    def run(self):
        try:
            self.query()
        except:
            self.stopQuery()
            import systems
            systems.terminal.output("Query operation failed.")



    querystep = 0
    querydata = ()
    def startQuery(self):
        self.asynsock.clear()
        self.querystep = 1
    def stopQuery(self):
        self.querystep = 0
        self.querydata = ()
    def query(self):
        if self.querystep:
            asynsock = self.asynsock

            # Step one
            if self.querystep == 1:
                if not asynsock.connected:
                    asynsock.connect()
                else:
                    asynsock.send( ("QUERY", 1) )
                    self.querystep = 2

            # Step two
            if self.querystep == 2:
                sent = asynsock.send()
                if sent:
                    self.querystep = 3

            # Step three
            if self.querystep == 3:
                packages = asynsock.recv()
                if packages:
                    infopack = packages[0]
                    import comms
                    datapair = comms.unpack(infopack)
                    self.querydata = datapair

                    asynsock.send( ("CLOSE", 1) )
                    self.querystep = 4

            # Step four
            if self.querystep == 4:
                sent = asynsock.send()
                if sent:
                    asynsock.clear()
                    self.querystep = 0

                    import systems
                    data = self.querydata[1]
                    for key in data:
                        out = "%s: %s" % (key, data[key])
                        systems.terminal.output(out)

                    self.querystep = 0
                    return self.querydata
            return None





Handler = HANDLER()





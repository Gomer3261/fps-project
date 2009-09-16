class ASYNSOCK:
    import comms
    import time

    instream = comms.STREAM()
    outpipe = ""

    lastTime = time.time()

    sock = None
    connected = 0
    connecting = 0

    def setLastTime(self):
        time = self.time
        self.lastTime = time.time()

    def goneStale(self, timeout=10.0):
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

    def connect(self, ip="chase.kicks-ass.net", port=2340, timeout=10.0):
        if not self.sock:
            self.createSocket()

        if self.connecting:
            if self.goneStale(timeout):
                self.sock = None
                self.connected = 0
                self.connecting = 0
                raise Exception, "Connection operation went stale"
            else:
                try:
                    peer = self.sock.getpeername()
                    if peer:
                        # We're connected!
                        self.connected = 1
                        self.connecting = 0
                        return 1 # This means we are successfully connected!
                except:
                    pass

        # Not connecting, so we must start connecting
        else:
            try:
                self.sock.connect( (ip, port) )
            except:
                pass
            self.connecting = 1
            self.setLastTime()

        return 0 # This means the connection operation is still in progress (this method must be run again)

    def recv(self, buf=2048, timeout=21.0):
        if not self.connected:
            raise Exception, "Cannot recv(); Not connected"

        if not self.goneStale(timeout):
            try:
                data = self.sock.recv(buf)
                if data:
                    self.setLastTime()
                    self.instream.push(data)
                    packages = self.instream.extract()
                    return packages
            except:
                pass
        else: # Gone stale!
            raise Exception, "Gone stale on recv()"

        return [] # No data.

    def send(self, flag, data):
        if not self.connected:
            raise Exception, "Cannot send(); Not connected"

        package = self.comms.pack(flag, data)
        self.outpipe += package

        self.setLastTime()

        self.sendloop()

    def sendloop(self, timeout=21.0):
        if not self.goneStale(timeout):
            if self.outpipe:
                try:
                    sent = self.sock.send(self.outpipe)
                    self.outpipe = self.outpipe[sent:]
                    if sent:
                        self.setLastTime()
                except:
                    pass
            else: # Not outpipe:
                return 1 # All data sent.
        else:
            # Gone stale
            raise Exception, "Gone stale on send()"

        return 0 # Send operation still in progress

    def clear(self):
        if self.connected:
            self.sock.close()
        self.sock = None
        self.connected = 0
        self.connecting = 0
        self.setLastTime()
        self.instream = self.comms.STREAM()
        self.outstream = ""

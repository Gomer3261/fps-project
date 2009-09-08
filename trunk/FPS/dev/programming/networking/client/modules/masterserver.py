class MASTERSERVER:
    LIFE = 1

    TCP = None
    connected = 0
    connecting = 0

    import comms
    import time

    stream = comms.STREAM()
    outpipe = ""

    lastcontact = time.time()
    ejectiontime = 240.0

    def connect(self, host, port):
        import socket
        try:
            self.TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.TCP.setNonBlocking()
            try:
                self.TCP.connect( (host, port) )
            except:
                self.connecting = 1
            peer = self.TCP.getpeername()
            if peer:
                self.connected = 1
                self.connecting = 0
        except:
            self.connected = 0
            print "Could not connect to Master Server."

    def setNonBlocking(self):
        self.TCP.setblocking(0)
        self.TCP.settimeout(0.0)

    def recv(self, buf=2048):
        try:
            data = self.TCP.recv(buf)
            if data:
                self.stream.push(data)
                self.lastcontact = self.time.time()
            return self.stream.extract()
        except:
            return []

    def send(self, flag, data):
        try:
            package = self.comms.pack(flag, data)
            self.outpipe += package
            sent = self.TCP.send(self.outpipe)
            self.outpipe = self.outpipe[sent:]
            return 1
        except:
            return 0

    def sendloop(self):
        if self.outpipe:
            try:
                sent = self.TCP.send(self.outpipe)
                self.outpipe = self.outpipe[sent:]
                return 0
            except:
                pass
        else:
            return 1

    def terminate(self):
        self.TCP.close()
        self.connected = 0
        self.LIFE = 0

masterserver = MASTERSERVER()

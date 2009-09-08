class CLIENT:
    LIFE = 1

    import comms
    import time

    stream = comms.STREAM()
    outpipe = ""

    TCP = None
    UDP = None

    UDP_addr = None

    connected = 0

    def __init__(self, expiration=5.0):
        self.expiration = expiration
        self.lastcontact = self.time.time()

    def contact(self):
        self.lastcontact = self.time.time()

    # Connect over TCP, and optionally prepare a UDP socket at the same time.
    def connect(self, host="chase.kicks-ass.net", TCPport=2342, UDPport=2343):
        self.host = host
        self.TCPport = TCPport
        
        self.UDPport = UDPport
        self.UDP_addr = (host, UDPport)
        
        import socket
        #import traceback
        try:
            self.TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.TCP.setblocking(1)
            self.TCP.settimeout(self.expiration)
            self.TCP.connect( (host, TCPport) )

            self.UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            self.connected = 1
            self.setNonBlocking()

            self.contact()
            return 1 # Connected :D
        except:
            self.connected = 0
            return 0 # Not Connected :(

    def setNonBlocking(self):
        self.TCP.settimeout(0.0)
        self.TCP.setblocking(0)
        if self.UDP:
            self.UDP.settimeout(0.0)
            self.UDP.setblocking(0)

    def recv(self, buf=2048):
        try:
            data = self.TCP.recv(buf)
            if data:
                self.stream.push(data)
                self.contact()
            packages = self.stream.extract()
            items = self.comms.unpackList(packages)
            return items
        except:
            return []

    def catch(self, buf=8192):
        try:
            package, addr = self.UDP.recvfrom(buf)
            if package:
                flag, data = self.comms.unpack(package)
                self.contact()
                return flag, data
        except:
            pass

    def getItems(self):
        items = []
        
        TCP_items = self.recv()
        UDP_item = self.catch()

        for item in TCP_items:
            items.append(item)

        if UDP_item:
            items.append(UDP_item)

        return items

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

    def throw(self, ticket, flag, data):
        try:
            import comms
            package = comms.packUDP(ticket, flag, data)
            self.UDP.sendto(package, self.UDP_addr)
        except:
            pass
    
    def terminate(self):
        if self.TCP:
            self.TCP.close()
        if self.UDP:
            self.UDP.close()
        self.connected = 0
        self.LIFE = 0

    def isStale(self):
        dif = self.time.time() - self.lastcontact
        if dif > self.expiration:
            return 1 # is stale
        else:
            return 0 # not stale

    def terminateIfStale(self):
        stale = self.isStale()
        if stale:
            print "Connection to gameplay server went stale."
            self.terminate()
            return 1 # Terminated
        else:
            return 0 # Not terminated


















class SERVER:
    LIFE = 1

    import comms
    import time

    TCP = None
    UDP = None
    
    bound = 0
    
    def bind(self, TCPport, UDPport=None):
        import socket

        self.TCPport = TCPport
        self.UDPport = UDPport
        
        self.TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCP.bind( ("", TCPport) )

        if UDPport:
            self.UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.UDP.bind( ("", UDPport) )
        
        self.setNonBlocking()
        self.bound = 1

    def setNonBlocking(self):
        self.TCP.setblocking(0)
        self.TCP.settimeout(0.0)

        if self.UDP:
            self.UDP.setblocking(0)
            self.UDP.settimeout(0.0)

    def accept(self):
        try:
            self.TCP.listen(1)
            connection = self.TCP.accept()
            return connection
        except:
            pass

    def throw(self, flag, data, addr):
        try:
            import comms
            package = comms.pack(flag, data)
            self.UDP.sendto(package, addr)
        except:
            pass

    def catch(self, buf=8192):
        try:
            package, addr = self.UDP.recvfrom(buf)
            
            ticket, flag, data = self.comms.unpackUDP(package)
            return ticket, flag, data, addr
        except:
            return None

    def terminate(self):
        if self.TCP:
            self.TCP.close()
        if self.UDP:
            self.UDP.close()
        
        self.TCP = None
        self.UDP = None
        
        self.bound = 0
        self.LIFE = 0

















class CLIENTHANDLER:
    LIFE = 1

    info = {}

    import comms
    import time

    connection = None
    sock = None
    UDP_addr = None

    stream = comms.STREAM()
    outpipe = ""
    catchpipe = []

    lastcontact = time.time()




    ### ================================================
    ### INITIATION
    ### ================================================
    # connection: The TCP Connection given by the server socket on accept()
    # owner: The server socket that this client came from. This server socket is used for UDP communications.
    # expiration: The timeout required for the clienthandler to go "stale".
    def __init__(self, connection, owner, expiration=5.0):
        # Connection related stuff
        self.connection = connection
        self.sock = self.connection[0] # sock always refers to TCP socket
        self.TCP_addr = self.connection[1]
        self.ip = self.TCP_addr[0]

        # Owner server socket
        self.owner = owner

        # Expiration timeout time
        self.expiration = expiration

        # Now we set to nonblocking
        self.setNonBlocking()
        self.contact()




    ### ================================================
    ### BASIC FUNCTIONS
    ### ================================================
    def setNonBlocking(self):
        self.sock.setblocking(0)
        self.sock.settimeout(0.0)

    def terminate(self):
        self.sock.close()
        self.LIFE = 0

    def isStale(self):
        dif = self.time.time() - self.lastcontact
        if dif > self.expiration:
            return 1 # is stale
        else:
            return 0 # not stale

    def terminateIfStale(self):
        stale = self.isStale()
        if stale:
            print "Client handler went stale. Terminated."
            self.terminate()

    def contact(self):
        self.lastcontact = self.time.time()




    ### ================================================
    ### COMMUNICATION FUNCTIONS
    ### ================================================

    def recv(self, buf=2048):
        try:
            data = self.sock.recv(buf)
            if data:
                self.stream.push(data)
                self.contact()
            packages = self.stream.extract()
            items = self.comms.unpackList(packages)
            return items
        except:
            return []

    def send(self, flag, data):
        try:
            package = self.comms.pack(flag, data)
            self.outpipe += package
            sent = self.sock.send(self.outpipe)
            self.outpipe = self.outpipe[sent:]
            return 1
        except:
            return 0

    def sendloop(self):
        if self.outpipe:
            try:
                sent = self.sock.send(self.outpipe)
                self.outpipe = self.outpipe[sent:]
            except:
                pass

    def throw(self, flag, data):
        addr = self.UDP_addr
        if not addr:
            print "        UDP_addr error."
            return None
        self.owner.throw(flag, data, addr)

    def catch(self):
        catches = self.catchpipe
        self.catchpipe = []
        if catches:
            self.contact()
        return catches

    # For distributing a catch
    # (The clienthandler doesn't do any UDP communication;
    # it's all done through the server socket (clienthandler.owner),
    # so this is the server socket's way of giving the clienthandler it's
    # UDP messages.
    def distroCatch(self, flag, data):
        self.catchpipe.append( (flag, data) )

    def getItems(self, buf=2048):
        items = []

        # An item looks like this: (flag, data)

        TCP_items = self.recv(buf)
        UDP_items = self.catch()

        for item in TCP_items:
            items.append(item)

        for item in UDP_items:
            items.append(item)

        return items

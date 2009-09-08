#################################################
###### ------ MASTER SERVER CLASSES ------ ######
#################################################
### Copyright 2009 Chase Moskal


class MASTERSERVERSOCKETS:
    LIFE = 1
    import socket
    import time
    import comms

    def __init__(self, cport=2340, sport=2341):
        socket = self.socket

        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.bind( ("", cport) )
        
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind( ("", sport) )

        self.setNonblocking()

    def setNonblocking(self):
        self.clientsocket.setblocking(0)
        self.clientsocket.settimeout(0.0)
        
        self.serversocket.setblocking(0)
        self.serversocket.settimeout(0.0)

    def acceptClient(self):
        try:
            self.clientsocket.listen(1)
            connection = self.clientsocket.accept()
            return connection
        except:
            return None

    def acceptServer(self):
        try:
            self.serversocket.listen(1)
            connection = self.serversocket.accept()
            return connection
        except:
            return None

    def acceptConnections(self):
        newClientConnection = self.acceptClient()
        newServerConnection = self.acceptServer()
        return newClientConnection, newServerConnection

    def terminate(self):
        print ">>> Terminating MasterServer Sockets..."
        self.clientsocket.close()
        self.serversocket.close()
        self.LIFE = 0







class HANDLER:
    LIFE = 1
    import comms
    import time

    info = {}

    def __init__(self, connection, ejectiontime=10.0):
        self.connection = connection
        self.sock = connection[0]
        self.addr = connection[1]
        self.ip = self.addr[0]

        self.stream = self.comms.STREAM()
        self.outpipe = ""

        self.ejectiontime = ejectiontime
        self.lastcontact = self.time.time()

        # Set to nonblocking
        self.setNonblocking()

    def setNonblocking(self):
        self.sock.setblocking(0)
        self.sock.settimeout(0.0)

    def recv(self, buf=2048):
        import traceback
        try:
            data = self.sock.recv(buf)
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
                return 0
            except:
                pass
        else:
            return 1
    
    def terminateIfStale(self):
        dif = self.time.time() - self.lastcontact
        if dif > self.ejectiontime:
            self.terminate()
            return 1 # has gone stale
        else:
            return 0 # has not gone stale

    def terminate(self):
        self.sock.close()
        self.LIFE = 0

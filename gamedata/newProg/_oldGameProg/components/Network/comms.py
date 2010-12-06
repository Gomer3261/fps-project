#############################################
### ------ COMMUNICATION FUNCTIONS ------ ###
#############################################

import pickle

packsep = "\x11" # DC1
########## Useless, but still cool
a = "\x12" # DC2
b = "\x13" # DC3
c = "\x14" # DC4
##########

def pack(data):
	package = pickle.dumps(data) + packsep
	return package

def packUDP(data):
	# Same as pack, but no packseparator for buffers
    udpPackage = pickle.dumps(data)
    return udpPackage

def unpack(package):
    data = pickle.loads(package)
    return data

def unpackList(packages):
    """
    Only for TCP Packages
    """
    items = []
    for package in packages:
        data = unpack(package)
        items.append( data )
    return items



def makeAddressTuple(address="IPADDR:TCPPORT/UDPPORT"):
	#print("mAT(a):",address)
	IP, ballsack, ports = address.partition(":")
	if "/" in ports:
		ports = ports.split("/")
		tcpPort, udpPort = ports
		tcpPort = eval(tcpPort)
		udpPort = eval(udpPort)
		#print("mAT(b):",IP,tcpPort,udpPort)
		return IP, tcpPort, udpPort
	else:
		port = eval(ports)
		#print("mAT(b):",IP,port)
		return IP, port

def makeAddressString(address=('IPADDR', 1001, 1001)):
	items = []
	for i in address: items.append(str(i))
	IP = items.pop(0)
	ports = "/".join(items)
	return IP + ":" + ports



# Simple timer object. Does this belong here?
class TIMER:
    def __init__(self):
        import time
        self.time = time
        self.lastTime = self.time.time()
    def get(self):
        return self.time.time() - self.lastTime
    def reset(self, target=0.0):
        self.lastTime = self.time.time()-target




class STREAM:
    """
    A kind of buffer. Used for extracting packages from an ongoing stream of information.
	TCP anyone?
    """
    def __init__(self):
        self.content = ""

    def add(self, data):
        self.content += data

    def push(self, data):
        """
        Synonymous with add(data).
        """
        self.content += data

    def extract(self):
        """
        Extracts whole valid packages from the buffer.
        """
        packs = []
        
        chunks = self.content.split(packsep)
        lastchunk = chunks[len(chunks)-1]
        chunks = chunks[:len(chunks)-1]
        for chunk in chunks:
            if chunk:
                packs.append(chunk+packsep)
        self.content = lastchunk
        return packs

    def clear(self):
        self.content = ""


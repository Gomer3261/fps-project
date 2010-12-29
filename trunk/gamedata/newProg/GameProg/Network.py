Server=None # Server Object.
Client=None # Client Object.
inBuffer=[] # List of messages that Network has recieved.




class initiateServer:
	def __init__(self,port):
		import socket
		self.buf=1024
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(('',port))
		
		connections = {} # Dictionary of connections
		
		#self.nextTicket=0
	#def getTicket(self): t=self.nextTicket; self.nextTicket+=1; return t
	
	class makeConnection:
		def __init__(self,addr):
			#self.ticket=ticket
			self.addr=addr
			self.throwInSeq=0; self.throwOutSeq=0
			self.sendInSeq=0; self.sendOutSeq=0
	
	def lowLevelStuff(self):
		import netfuncs
		data,addr = self.sock.recvfrom(self.buf)
		if data:
			if data[0]=="\x11": # It's a network message.
				if data[1] == "c": # they want to initiate a connection.
					self.connections[addr] = self.makeConnection(addr)
					packet = netfuncs.makeNetPacket('a', newTicket, payload):
					self.sock.sendto(packet,addr)







class initiateClient:
	def __init__(self,addr,port):
		pass



def acceptConnections():
	pass
	return newUsers


def catchMessages():
	pass
	return messages

def addToInBuffer(messages):
	global inBuffer
	for message in messages:
		inBuffer.append(message)

def send():
	"Reliable UDP"
	pass


def throw():
	"Unreliable UDP"
	pass

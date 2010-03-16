### Networking Classes ###


###### ### #################### ### ######
###### ### ### HIGH CLASSES ### ### ######
###### ### #################### ### ######

class MS_SERVER:
	pass



class GPS_SERVER:
	"""
	The GamePlay Server Object.
	Maintains a TCP_SERVER object, and a UDP_SERVER object simultaneously, while
	serving as a full communications processing center with a simple public interface
	for communicating with client, and for and server functions. Includes awesome 
	features like temporarily saving client sessions to allow for client session 
	recoveries.
	It's primarily a TCP server, but it has a UDP server as a supplement; all of the
	important things are done through TCP, the UDP is an added bonus that requires 
	the TCP in order to work.
	
	TODO:
		Implement some form of the old 'Theater' system for maintaining sessions.
	
	"""
	def __init__(self, address="192.168.1.1:3201/3202", TCP_SERVER, UDP_SERVER):
	
		### Deciphering Addrs ###
		try:
			if not ':' in address:
				address = ':' + address
			host, ports = address.split(':')
			tcpPort, udpPort = ports.split('/')
			tcpAddr = host, tcpPort
			udpAddr = host, udpPort
			self.host = host
			self.tcpPort = tcpPort
			self.udpPort = udpPort
		except:
			print("\nThere was an error deciphering addrs (Networking/classes.GPS_SERVER.__init__).")
			import traceback
			traceback.print_exc()
		
		# Initiating Server
		try:
			self.tcpServer = TCP_SERVER(tcpAddr)
			self.udpServer = UDP_SERVER(udpAddr)
			print("Server is Initiated")
		except:
			print("\nThere was an error initiating the server (Networking/classes.GPS_SERVER.__init__).")
			import traceback
			traceback.print_exc()
	
	
	def run(self):
		# Accept new TCP clients
		newConnection = self.tcpServer.acceptNewConnection()
		if newConnection:
			newTcpClientHandler = TCP_CLIENT_HANDLER( newConnection )
			# Make it into a new session?
		







class MS_CLIENT:
	pass




class GPS_CLIENT:
	pass






###### ### ##################### ### ######
###### ### ### BASIC CLASSES ### ### ######
###### ### ##################### ### ######

class TCP_SERVER:
	def __init__(self, address):
		import socket
		self.socket = socket
		self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serverSock.bind(address)
	
	def acceptNewConnection(self):
		self.serverSock.listen(1)
		connection = self.serverSock.accept()
		return connection




class UDP_SERVER:
	def __init__(self, address):
		import socket
		self.socket = socket
		self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.serverSock.bind(address)




class TCP_CLIENT:
	pass



class UDP_CLIENT:
	pass





###### ### ################### ### ######
###### ### ### SUB CLASSES ### ### ######
###### ### ################### ### ######
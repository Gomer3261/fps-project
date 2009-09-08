import socket
import comms

host = "chase.kicks-ass.net"
port = 2340

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect( (host, port) )

data = {}
data["name"] = "chase"
data["password"] = "password"
data["email"] = "email@email.egg"

sock.sendall( comms.pack("login", data) )

data = sock.recv(4096)

print data

sock.sendall( comms.pack("CLOSE", 1) )

sock.close()

print "DONE"

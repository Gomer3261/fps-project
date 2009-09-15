import socket
import comms

host = "chase.kicks-ass.net"
port = 2340

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect( (host, port) )

sock.sendall( comms.pack("terminate", 1) )

sock.close()

print "DONE"

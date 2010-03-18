import classes

address = ("", 3205)
server = classes.TCP_SERVER(address)
while 1:
	newConnection = server.acceptNewConnection()

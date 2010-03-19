import classes

address = ("", 3205)
server = classes.TCP_SERVER(address)
bound = server.bind()
if bound:
	print("Server bound.")
	run = True
	while run:
		bundles, newConnections, staleClients, staleSessions = server.run()
		for bundle in bundles:
			ticket, item = bundle
			flag, data = item
			
			if flag == 'MSG':
				print("Message from %s: %s"%(ticket, data))
			
			if flag == 'COM': # It's a command!
				if data == 'TERMINATE':
					print("Received command to terminate from %s."%(ticket))
					session = server.getSession(ticket)
					session.clientSock.send( ('COM', 'TERMINATE') )
					session.terminateClientSock()
					run = False # Oh Noes!
else:
	print("Binding failure.")

print("Over and out.")
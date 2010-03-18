import classes

address = ("", 3205)
server = classes.TCP_SERVER(address)
run = True
while run:
	bundles = server.run()
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

print("Over and out.")
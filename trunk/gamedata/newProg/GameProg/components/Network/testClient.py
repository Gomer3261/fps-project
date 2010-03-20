import classes

address = ("96.54.129.113", 3205)
client = classes.TCP_CLIENT(address)
client.initiateConnection(); print("Connection operation initiated.")

client.send( ('MSG', 'Hello!') )
client.send( ('MSG', 'World!!!') )

run = True
while run:
	items, hasGoneStale, justConnected = client.run()
	if justConnected: print("Just Connected!")
	for item in items:
		flag, data = item
		if flag == 'MSG':
			print("Message from server: %s"%(data))
		if (flag == 'COM') and (data == 'TERMINATE'):
			print("Got Termination Command.")
			client.terminate()
			run = False
	if hasGoneStale:
		print("STALE!")
		client.terminate()
		run = False

print("Job Done.")

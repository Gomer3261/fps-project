import classes

address = ("96.54.129.113", 3205)
client = classes.TCP_CLIENT(address)
client.send( ('MSG', 'Hi!') )
client.send( ('COM', 'TERMINATE') )

run = True
while run:
	items, hasGoneStale = client.run()
	for item in items:
		flag, data = item
		if flag == 'MSG':
			print("Message from server: %s"%(data))
		if (flag == 'COM') and (data == 'TERMINATE'):
			print("Got Termination Command.")
			client.terminate()
			run = False
	if hasGoneStale:
		print("Connection went stale.")
		client.terminate()
		run = False

print("Job Done.")

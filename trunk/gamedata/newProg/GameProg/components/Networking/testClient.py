import classes

address = ("96.54.129.113", 3205)
sock = classes.TCP_CLIENT(address)
while 1:
	sock.run()
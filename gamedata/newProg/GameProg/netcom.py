codes = {}
codes['net'] = '\x11'
codes['throw'] = '\x12'
codes['stream'] = '\x13'
codes['sep'] = '\x14'

def makeSeqStr(integer):
	return "%010d"%integer

def makeIdStr(integer):
	return "%05d"%integer


def serverBuildThrowPacket(seq, payload):
	packet = codes['throw']
	packet+= str(seq) + codes['sep']
	packet+= payload
	return packet


def serverParseThrowPacket(packet):
	flag = packet[0]
	maindata = packet[1:]
	seqStr, idStr, payload = maindata.split( codes['sep'] )
	seq=int(seqStr); id=int(idStr)
	return seq, id, payload


def clientBuildThrowPacket(seq, id, payload):
	packet = codes['throw']
	packet+= str(seq) + codes['sep']
	packet+= str(id) + codes['sep']
	packet+= payload
	return packet


def clientParseThrowPacket(packet):
	flag = packet[0]
	maindata = packet[1:]
	seqStr, payload = maindata.split( codes['sep'] )
	seq=int(seqStr)
	return seq, payload





def sendStream():
	pass

def recvStream():
	pass
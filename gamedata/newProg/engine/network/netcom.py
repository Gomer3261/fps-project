import pickle

codes = {}
codes['net'] = b'\x11'
codes['throw'] = b'\x12'
codes['stream'] = b'\x13'
codes['sep'] = b'\x14'


def serverBuildThrowPacket(seq, payload):
	packet = codes['throw']
	packet+= bytes(seq) + codes['sep']
	packet+= pickle.dumps( payload )
	return packet


def serverParseThrowPacket(packet):
	flag = packet[0]
	maindata = packet[1:]
	seqStr, idStr, payload = maindata.split( codes['sep'] )
	seq=int(seqStr); id=int(idStr)
	return seq, id, pickle.loads( payload )


def clientBuildThrowPacket(seq, id, payload):
	packet = codes['throw']
	packet+= bytes(seq) + codes['sep']
	packet+= bytes(id) + codes['sep']
	packet+= pickle.dumps( payload )
	return packet


def clientParseThrowPacket(packet):
	flag = packet[0]
	maindata = packet[1:]
	seqStr, payload = maindata.split( codes['sep'] )
	seq=int(seqStr)
	return seq, pickle.loads( payload )





def sendStream():
	pass

def recvStream():
	pass
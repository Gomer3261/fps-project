import pickle

def pack(data):
	return pickle.dumps( data )

def unpack(packet):
	return pickle.loads( packet )







#######
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
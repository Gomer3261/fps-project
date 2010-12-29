
def makeSeq(integer):
	return "%010d"%integer

def makeNetPacket(data):
	return "\x11" + data


def makeThrowPacket(seqInt, data):
	return "\x12" + makeSeq(seqInt) + data


def makeSendPacket(seqInt, data):
	return "\x13" + makeSeqInt(seqInt) + data
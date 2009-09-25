mode = "offline"
ticket = 0
inGame = 0

def set(newMode="offline"):
	global mode
	global ticket
	global inGame
	
	mode = newMode
	ticket = 0
	inGame = 0

def weAreTheHost():
	global mode
	if mode == "online":
		return 0
	else:
		return 1
####################################
### ------	TERMINAL	  ------ ###
####################################
### Copyright 2009 Chase Moskal!
# This is the terminal module.
# It handles terminal input and output.

INIT = 1




# Terminal access activitiy.
active = 0

# The contents of the terminal window (output)
openingText = """Welcome to the terminal!

Remember:
   Precede all python commands with a slash (/), otherwise it is regarded as a text message.

Important functions:
	/defaultOptions() # Use this whenever things seem to be not working.
	/listUserCommands()
	/help(cmd)
	/connect("YourName", stokes) # 'stokes' is the server, you can also use 'chase' or 'geoff'
	/disconnect() # disconnects you from the gameplay server.
	/users() # outputs a list of users in the game.
	/players() # outputs a list of players currently alive.
	/info() # gives you game information.
	/ammo() # gives you information about your ammunition.

Tip: Your first magazine is loaded with 3000 rounds, for debug reasons.
Game developers don't need to reload.

================================================================
"""

openingText = openingText.replace("\r", "")
contents = openingText.split("\n")
oldcontents = []

# Variables for handling the history
history = []
history_slot = 0
HISTORY_MAX = 10
current_input = ""



# For opening and closing the terminal (detects single presses)
termkeyLast = 0

wraplen = 100
maxlines = 60










######################################
### ------ TERMINAL HISTORY ------ ###
######################################

# Saves a string to the history
def addToHistory(s):
	global history, HISTORY_MAX

	history.insert(0, s)
	
	history_slot = -1
	
	if len(history) > HISTORY_MAX:
		history.remove(history[-1])

# Saves the current input so it can be recovered
def saveCurrentInput(s):
	global current_input
	current_input = s

# Gets the next item in the history

def getNextHistoryItem(s):
	global history, HISTORY_MAX, history_slot
	history_slot += 1
	
	if history_slot == 0:
		saveCurrentInput(s)
	elif history_slot > HISTORY_MAX:
		history_slot = 0
	elif (len(history)-1) < history_slot:
		history_slot = len(history) - 1
		

	return history[history_slot]

# Gets the previous item in the history
def getPrevHistoryItem():
	global history, HISTORY_MAX, history_slot, current_input
	history_slot -= 1
	
	if history_slot < 0:
		history_slot = -1
		return current_input
	
	return history[history_slot]











#########################################
### ------ TERMINAL FORMATTING ------ ###
#########################################

# Trims a list from the beginning until it reaches the desired length.
def limit(x, l=10):
	while len(x) > l:
		x = x[1:]
	return x

# Formats lines (wraps them, trims them)
def formatLines(lines):
	import textwrap
	newlines = []

	for line in lines:
		new = textwrap.fill(line, wraplen).split("\n")
		for n in new:
			newlines.append(n)

	newlines = limit(newlines, maxlines)

	return newlines

## -- Deprecated Functions -- ##

### Limits the number of lines of contents it remembers.
##def limitContents(l=10):
##	  global contents
##	  contents = limit(contents, l)
##
### Takes a string and cuts it into n sized chunks (returns a list)
##def textwrap(s, n):
##	  return [s[x:x+n] for x in range (0, len(s), n)]

### Formats contents into a string, and outputs it.
##def getContents(lines=10, wrap=50):
##	  global contents
##	  
##	  data = []
##	  for line in contents:
##		  linestart = 1
##		  for x in textwrap(line, wrap):
##			  if linestart:
##				  data.append(x)
##			  else:
##				  data.append("	   "+x)
##			  linestart = 0
##	  return "\n".join(limit(data, lines))










########################################
### ------ TERMINAL FUNCTIONS ------ ###
########################################

# runs input commands (maybe rename to run, or command?)
def input(s):
	isCommand = 0
	if s[0] == "/":
		isCommand = 1
	
	if isCommand:
		output(" ")
		output(">> "+s)
		s = s[1:]
		
		import commandsUser
		import commandsAdmin
		modules = [commandsUser, commandsAdmin]

		namespace = {}
		
		for module in modules:
			for variableName in dir(module):
				namespace[variableName] = getattr(module, variableName)

		import sys
		import traceback
		try:
			exec(s, namespace)
		except:
			error = traceback.format_exception_only(sys.exc_type, sys.exc_value)
			error = error[len(error)-1]
			output(error)
	else:
		import modules
		modules.networking.gncore.text(s)

# Outputs something to the terminal.
def output(s):
	global contents
	
	s = s.replace("\r", "")
	lines = s.split("\n")

	for line in lines:
		contents.append(line)

# Clears terminal's contents.
def clear():
	global contents
	contents = []










######################################
### ------ TERMINAL HANDLER ------ ###
######################################

def runHandler(con):
	global contents
	global active
	global oldcontents
	
	returnKey = con.sensors["RETURN"]
	upKey = con.sensors["UP"]
	downKey = con.sensors["DOWN"]
	deleteKey = con.sensors["DELETE"]

	inTextObj = con.actuators["inText"].owner
	outTextObj = con.actuators["outText"].owner


	### INPUT HANDLING ###

	# Delete key clears input field
	if deleteKey.positive:
		inTextObj["input"] = ""
	
	# A = Input String
	A = inTextObj["input"]
	A = A.replace("\r", "")
	A = A.replace("\n", "")
	inTextObj["Text"] = A + "|"

	
	if A and returnKey.positive:
		input(A)
		inTextObj["input"] = ""
		inTextObj["Text"] = ""
		
		# Add the last input into the history
		addToHistory(A)

		
		
	elif upKey.positive:
		inTextObj["input"] = getNextHistoryItem(A)
	elif downKey.positive:
		inTextObj["input"] = getPrevHistoryItem()
	
	if oldcontents != contents:
		### OUTPUT HANDLING ###
		contents = formatLines(contents)
		output = "\n".join(contents)
		
		output = output.replace("\r", "")
		
		outTextObj["Text"] = output
		oldcontents = contents[:]



def handleOpenClose(con):
	global active
	global termkeyLast
	global oldcontents
	
	termkey = con.sensors["termkey"]

	if termkey.positive and (not termkeyLast):
		if active:
			closeTerminal = con.actuators["closeTerminal"]
			con.activate(closeTerminal)
			active = 0
		else:
			openTerminal = con.actuators["openTerminal"]
			con.activate(openTerminal)
			active = 1
			oldcontents = []

	termkeyLast = termkey.positive

####################################
### ------  TERMINAL      ------ ###
####################################
### Copyright 2009 Chase Moskal!
# This is the terminal module.
# It handles terminal input and output.

INIT = 1




# Terminal access activitiy.
active = 0

# The contents of the terminal window (output)
contents = ["Welcome to the terminal! Type help() if you're new here."]

# Terminal input pipe
inpipe = []

# Variables for handling the history
history = []
history_slot = 0
HISTORY_MAX = 10
current_input = ""



# For opening and closing the terminal (detects single presses)
termkeyLast = 0

wraplen = 100
maxlines = 60




# Methods for handling the history

# Saves a string to the history
def addToHistory(s):
    global history, HISTORY_MAX

    history.insert(0, s)
    
    history_slot = -1
    
    if len(history) > HISTORY_MAX:
        history.remove(-1)

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
        new = textwrap.wrap(line, wraplen)
        for n in new:
            newlines.append(n)

    newlines = limit(newlines, maxlines)

    return newlines

# Limits the number of lines of contents it remembers.
def limitContents(l=10):
    global contents
    contents = limit(contents, l)

# Takes a string and cuts it into n sized chunks (returns a list)
def textwrap(s, n):
    return [s[x:x+n] for x in range (0, len(s), n)]

# Formats contents into a string, and outputs it.
def getContents(lines=10, wrap=50):
    global contents
    
    data = []
    for line in contents:
        linestart = 1
        for x in textwrap(line, wrap):
            if linestart:
                data.append(x)
            else:
                data.append("    "+x)
            linestart = 0
    return "\n".join(limit(data, lines))

# Outputs something to the terminal
def output(s):
    global contents
    
    s = s.replace("\r", "")
    lines = s.split("\n")

    for line in lines:
        contents.append(line)



# Inputs a string to the inpipe
##def input(s):
##    global inpipe
##    inpipe.append(s)

def input(s):
    output(">> "+s)
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



# Enters something to the inpipe
def enter(s):
    global inpipe
    inpipe.append(s)

def clearInpipe():
    global inpipe
    inpipe = []

# Clears terminal's output contents
def clear():
    global contents
    contents = []












######### TERMINAL HANDLER ###########

def runHandler(con):
    global contents
    global inpipe
    global active
    
    returnKey = con.sensors["RETURN"]
    upKey = con.sensors["UP"]
    downKey = con.sensors["DOWN"]

    inTextObj = con.actuators["inText"].owner
    outTextObj = con.actuators["outText"].owner


    ### INPUT HANDLING ###
    
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
    


    ### OUTPUT HANDLING ###
    contents = formatLines(contents)
    output = "\n".join(contents)
    
    outTextObj["Text"] = output



def handleOpenClose(con):
    global active
    global termkeyLast
    
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

    termkeyLast = termkey.positive

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
contents = []

# Terminal input pipe
inpipe = []


wraplen = 100
maxlines = 60





# Trims a list from the beginning until it reaches the desired length.
def limit(x, l=10):
    while len(x) > l:
        x = x[1:]
    return x

# Formats lines (wraps them, trims them)
def formatLines(lines):
    import textwrap
    newlines = []

    import modules.profiling #######
    P = modules.profiling.PROFILE("formatLines") ######
    modules.profiling.SuperProfile.add(P)
    C = P.clock("for loop") ######

    for line in lines:
        new = textwrap.wrap(line, wraplen)
        for n in new:
            newlines.append(n)

    C.stop() ######
    #P.output() ######

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
    import modules.profiling
    prof = modules.profiling.PROFILE("terminal")
    modules.profiling.SuperProfile.add(prof)

    clockA = prof.clock("getting sensors and actuators") ########
    
    global contents
    global inpipe
    global active
    
    returnKey = con.sensors["RETURN"]

    inTextObj = con.actuators["inText"].owner
    outTextObj = con.actuators["outText"].owner
    
    clockA.stop() #########


    clockB = prof.clock("handling user input")
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
    
    clockB.stop()


    clockC = prof.clock("handling user output") ########
    ### OUTPUT HANDLING ###
    CA = prof.clock("calling formatLines()") ########
    contents = formatLines(contents)
    CA.stop() #########
    output = "\n".join(contents)
    
    outTextObj["Text"] = output
    clockC.stop() ##########


    modules.profiling.SuperProfile.output()

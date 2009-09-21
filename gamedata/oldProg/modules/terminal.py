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







# Trims a list from the beginning until it reaches the desired length.
def limit(x, l=10):
    while len(x) > l:
        del x[0]
    return x

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
def input(s):
    global inpipe
    inpipe.append(s)

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

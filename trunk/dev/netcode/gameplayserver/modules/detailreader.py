import sys
import traceback

path = sys.path[0] + "/serverdetails.txt"

def getDetails():
    try:
        info = {}
        
        f = open(path, "r")
        data = f.read()
        f.close()

        data = data.replace("\r\n", "\n")
        data = data.replace("\r", "\n")

        entrysep = "\n"
        elementsep = ":"

        entries = data.split(entrysep)
        for entry in entries:
            chunks = entry.split(elementsep)
            flag = chunks[0]
            del chunks[0]
            value = ":".join(chunks)

            info[flag] = value

        return info
    except:
        traceback.print_exc()
        return {}
